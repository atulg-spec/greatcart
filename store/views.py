from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery, RecentlyStalked, Variation
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
from search.models import top_searches, not_found_searches
from .utils import get_related_products, get_behavior_related_products

def store(request, category_slug=None):
    categories = None
    products = Product.objects.filter(is_available=True)
    notfoundsearches = not_found_searches.objects.all()

    # Filter by Category
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories)

    # Get available filter values
    sizes = Variation.objects.filter(
        product__in=products, variation_category='size', is_active=True
    ).values_list('variation_value', flat=True).distinct()

    colors = Variation.objects.filter(
        product__in=products, variation_category='color', is_active=True
    ).values_list('variation_value', flat=True).distinct()

    # Apply Filters based on user selection
    selected_size = request.GET.get('size')
    selected_color = request.GET.get('color')
    sort_by = request.GET.get('sort_by', '')

    if selected_size:
        products = products.filter(variation__variation_category='size', variation__variation_value=selected_size)

    if selected_color:
        products = products.filter(variation__variation_category='color', variation__variation_value=selected_color)

    # Apply Sorting
    if sort_by == 'popular':
        products = products.order_by('-stock')  # Assuming you track product views
    elif sort_by == 'new':
        products = products.order_by('-created_date')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'price_low_to_high':
        products = products.order_by('price')

    # Keyword Search
    keyword = request.GET.get('keyword', '')
    if keyword:
        # Split keywords into individual terms
        search_terms = keyword.split()
        
        # Start with an empty Q object
        queries = Q()
        
        for term in search_terms:
            queries |= Q(search_keywords=term)
            # queries |= Q(feature_category__name__icontains=term)
            # queries |= Q(category__category_name__icontains=term)
        
        products = products.filter(queries).distinct()

    # Pagination
    paginator = Paginator(products, 30)  
    page = request.GET.get('page', 1)

    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = []

    # Handle AJAX filter requests
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

    context = {
        'notfoundsearches': notfoundsearches,
        'products': paged_products,
        'sizes': sizes,
        'colors': colors,
        'category_slug': category_slug,
        'keyword': keyword,
        'selected_size': selected_size,
        'selected_color': selected_color,
        'sort_by': sort_by,
    }
    return render(request, 'store/store.html', context)

def search(request):
    topsearches = top_searches.objects.all()
    sections = homeSections.objects.all()
    context = {
        'topsearches': topsearches,
        'sections': sections,
    }
    return render(request, 'store/search.html',context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        related_products = get_related_products(single_product, 30)
        behaviour_related_products = get_behavior_related_products(single_product,request,30)
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
        'related_products': related_products,
        'behaviour_related_products': behaviour_related_products,
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
