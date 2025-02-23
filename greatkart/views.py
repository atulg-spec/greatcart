from django.shortcuts import render, get_object_or_404
from store.models import Product, ReviewRating
from home.models import Slider, homeSections, Page

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    mobile_sliders = Slider.objects.filter(is_mobile=True)
    desktop_sliders = Slider.objects.filter(is_mobile=False)
    sections = homeSections.objects.all()

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'mobile_sliders': mobile_sliders,
        'desktop_sliders': desktop_sliders,
        'sections': sections,
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)


def page_view(request, slug):
    # Fetch the product using the slug
    page = get_object_or_404(Page, slug=slug)
    context = {
        'page': page,
    }

    # Render the template with the context
    return render(request, 'page-view.html', context)
