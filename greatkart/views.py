from django.shortcuts import render
from store.models import Product, ReviewRating
from home.models import Slider, homeSections

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    sliders = Slider.objects.all()
    sections = homeSections.objects.all()

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'sliders': sliders,
        'sections': sections,
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)
