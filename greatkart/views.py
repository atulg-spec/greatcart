from django.shortcuts import render
from store.models import Product, ReviewRating
from home.models import Slider, homeSections

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
