# views.py
from django.shortcuts import render
from .models import advertisement
import random
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def render_ad(request):
    ads = advertisement.objects.all()
    ad = random.choice(ads) if ads else None
    return render(request, "ads/render.html", {"ad": ad})