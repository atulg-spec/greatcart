from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ReviewRating, RecentlyStalked
from home.models import Slider, homeSections, Page, featured_categories
from accounts.utils import phone_number_required
from notifications.models import SiteNotifications

def home(request):
    recently_stalked = None
    if request.user.is_authenticated:
        if not request.user.phone_number:
            return redirect('phone_number_registration')
        recently_stalked = RecentlyStalked.objects.filter(user=request.user)
    notification = None
    try:
        notification = SiteNotifications.objects.first()
    except:
        pass
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    mobile_sliders = Slider.objects.filter(is_mobile=True)
    desktop_sliders = Slider.objects.filter(is_mobile=False)
    features = featured_categories.objects.all()
    sections = homeSections.objects.all()

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'notification': notification,
        'mobile_sliders': mobile_sliders,
        'desktop_sliders': desktop_sliders,
        'sections': sections,
        'recently_stalked': recently_stalked,
        'features': features,
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
