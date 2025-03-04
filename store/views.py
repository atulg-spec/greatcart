from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery, RecentlyStalked
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from home.models import homeSections


def store(request, category_slug=None):
    categories = None
    products = None

    # Filter products based on category
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    # Filter products based on keyword
    keyword = request.GET.get('keyword', '')
    if keyword:
        products = products.filter(
            Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
        ).order_by('-created_date')

    # Pagination
    paginator = Paginator(products, 30)  # Show 30 products per page
    page = request.GET.get('page', 1)

    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paged_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        paged_products = []

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'products': [
                {
                    'id': product.id,
                    'name': product.product_name,
                    'price': product.price,
                    'sizes': [size for size in product.get_sizes()],
                    'before_discount_price': product.before_discount_price,
                    'image': product.images.url,
                    'stock': product.stock,
                    'secondary_image': product.secondary_image.url if product.secondary_image else None,
                    'url': product.get_url(),
                }
                for product in paged_products.reverse()
            ],
            'has_next': paged_products.has_next(),
            'category_slug': category_slug,
            'keyword': keyword,
        }
        return JsonResponse(data)

    # Render the template for non-AJAX requests
    context = {
        'products': paged_products,
        'category_slug': category_slug,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)

def search(request):
    sections = homeSections.objects.all()
    context = {
        'sections': sections,
    }
    return render(request, 'store/search.html',context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            RecentlyStalked.objects.create(user=request.user,product=single_product)
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)




def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
