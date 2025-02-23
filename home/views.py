from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from dashboard.models import *
from home.models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from dashboard.forms import ContactForm, CustomUserForm
import razorpay
from django.conf import settings
User = get_user_model()
# -=--------=---=----------=--=------PAGES--=---=------=---
# CONTACT US
@login_required
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request,'We will contact to you as soon as possible')
    return render(request,"home/contact.html")

# ABOUT
def about(request):
    return render(request,"home/about.html")

def disclaimer(request):
    return render(request,"home/disclaimer.html")

# POLICY
def privacypolicy(request):
    return render(request,"home/privacypolicy.html")

def refundpolicy(request):
    return render(request,"home/refundpolicy.html")

def termsofuse(request):
    return render(request,"home/termsofuse.html")

# END PAGES
def index(request):
    recent = None
    if request.user.is_authenticated:
        recent = RecentlyStalked.objects.filter(user=request.user)
    categories = Categories.objects.all()
    shop_categories = ProductByCategory.objects.all()
    new_products = Product.objects.filter(keywords__keyword__icontains='New').order_by('-id').distinct()[:30]
    top_products = Product.objects.filter(keywords__keyword__icontains='Top').order_by('-id').distinct()[:30]
    sale_products = Product.objects.filter(keywords__keyword__icontains='Sale').order_by('-id').distinct()[:30]
    context = {
        'recent':recent,
        'categories':categories,
        'shop_categories':shop_categories,
        'new_products':new_products,
        'top_products':top_products,
        'sale_products':sale_products,
    }
    return render(request,'home/index.html',context)

def search(request,search):
    query = search
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            models.Q(category__category__icontains=query) |  # Correct usage for ManyToManyField
            models.Q(description__icontains=query) |
            models.Q(keywords__keyword__icontains=query)
        ).distinct()[:100] 
    context = {
        'products':products,
        'search':search,
    }
    return render(request,'home/search.html',context)





def product_view(request, slug):
    # Fetch the product using the slug
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        RecentlyStalked.objects.create(user=request.user,product=product)
    
    # Get related data for the product
    product_images = ProductImage.objects.filter(product=product)
    stars = [i for i in range(0, product.stars)]
    categories = Categories.objects.all()

    # Fetch the first category for the query
    query = product.category.first().category if product.category.exists() else None

    # Initialize related products to none
    related_products = Product.objects.none()
    
    # If the query is not None, fetch related products
    if query:
        related_products = Product.objects.filter(
            models.Q(category__category__icontains=query) |  # Correct for ManyToManyField
            models.Q(description__icontains=query) |  # Correct for text field
            models.Q(keywords__keyword__icontains=query)  # Correct for ManyToManyField
        ).distinct()[:100]  # Avoid duplicate results

    # Pass the context to the template
    context = {
        'related_products': related_products,
        'categories': categories,
        'stars': stars,
        'product_images': product_images,
        'product': product,
    }

    # Render the template with the context
    return render(request, 'home/product-view.html', context)


@login_required
def add_to_cart(request,id,size,qty):
    product = Product.objects.filter(id=id).first()
    selected_size = Sizes.objects.filter(size=size).first()
    if product:
        exist = Cart.objects.filter(user=request.user,product=product).first()
        if not exist:
            Cart.objects.create(user=request.user,size=selected_size,product=product,quantity=qty)
    return redirect('/cart')

@login_required
def remove_item(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        product.delete()
    return redirect('/cart')

@login_required
def increase_quantity(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        product.quantity = product.quantity + 1
        product.save()
    return redirect('/cart')

@login_required
def decrease_quantity(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        try:
            if product.quantity < 2:
                messages.error(request,"Quantity can't be less than 1")
            else:
                product.quantity = product.quantity - 1
                product.save()
        except:
            messages.info(request,'Invalid details')
    return redirect('/cart')

@login_required
def cart(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    categories = Categories.objects.all()
    form = CustomUserForm(instance=request.user)
    cart_items = Cart.objects.filter(user=request.user).filter(ordered=False)
    total = 0
    for x in cart_items:
        total = total + x.product.price * x.quantity
    context = {
        'trending_products':trending_products,
        'form':form,
        'categories':categories,
        'total':total,
        'cart_items':cart_items,
    }
    return render(request,'home/cart.html',context)

# @login_required
# def create_order(request):
#     trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
#     cart_items = Cart.objects.filter(user=request.user).filter(ordered=False)
#     order = Order.objects.create(user=request.user)
#     order.products.set(cart_items)  # Use set() to assign the cart_items to the products field
#     categories = Categories.objects.all()
#     context = {
#         'trending_products':trending_products,
#         'categories':categories,
#     }
#     return redirect('/my-orders')

@login_required
def my_orders(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    orders = Order.objects.filter(user=request.user)
    categories = Categories.objects.all()
    print(orders)
    context = {
        'trending_products':trending_products,
        'categories':categories,
        'orders':orders,
    }
    return render(request,'home/orders.html',context)

def categories(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').distinct()[:50]
    categories = Categories.objects.all()
    context = {
        'trending_products':trending_products,
        'categories':categories,
    }
    return render(request,'home/categories.html',context)

@login_required
def track_order(request,id):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    order = Order.objects.filter(user=request.user,order_id=id).first()
    categories = Categories.objects.all()
    context = {
        'trending_products':trending_products,
        'categories':categories,
        'order':order,
    }
    return render(request,'home/track_order.html',context)

def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = Keywords.objects.none()
    if query:
        suggestions = Keywords.objects.filter(
            models.Q(keyword__icontains=query)
        ).reverse()        
    results = [
        s.keyword for s in suggestions if s.keyword
    ][:30]
    return JsonResponse(results, safe=False)

@csrf_exempt  # Use this only if you're not using {% csrf_token %} in the form, otherwise remove it
@login_required
def save_address(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        address = request.POST.get('address')
        user = User.objects.filter(email=request.user.email).first()
        user.phone_number = phone_number
        user.city = city
        user.state = state
        user.pin_code = pin_code
        user.address = address
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Address saved successfully!'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=405)




# Initialize Razorpay client
@login_required
def create_order(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)     
        if form.is_valid():
            form.save()
            gateway = PaymentGateway.objects.all().first()
            razorpay_client = razorpay.Client(auth=(gateway.razorpay_key_id, gateway.razorpay_key_secret))
            cart_items = Cart.objects.filter(user=request.user).filter(ordered=False)
            total = 0
            for x in cart_items:
                total = total + x.product.price * x.quantity
            total = int(total)
            order_data = {
                'amount': total * 100,
                'currency': 'INR',
                'payment_capture': 1
            }
            razorpay_order = razorpay_client.order.create(data=order_data)
            payment = Payment.objects.create(
                order_id=razorpay_order['id'],
                amount=total
            )

            context = {
                'cart_items':cart_items,
                'order_id': razorpay_order['id'],
                'razorpay_key': gateway.razorpay_key_id,
                'amount': total * 100,
                'total': total,
                'name': 'The Zainly',
                'email': request.user.email,
                'phone': request.user.phone_number
            }
            return render(request, 'home/payment.html', context)
    else:
        return redirect('/cart')


@csrf_exempt
def payment_verification(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        payment = Payment.objects.get(order_id=razorpay_order_id)
        gateway = PaymentGateway.objects.all().first()
        razorpay_client = razorpay.Client(auth=(gateway.razorpay_key_id, gateway.razorpay_key_secret))

        # Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Payment successful
            payment.payment_id = razorpay_payment_id
            payment.status = 'paid'
            payment.save()

            return render(request, 'payment_success.html')

        except:
            # Payment failed
            payment.status = 'failed'
            payment.save()
            return redirect('/')