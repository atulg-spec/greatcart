from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now, timedelta
from .models import SiteSettings, HeadSection, SideNav

def custom_site_context(request):
    head = HeadSection.objects.all().first()
    settings = SiteSettings.objects.all().first()
    side_nav = SideNav.objects.all()
    context = {
        'head':head,
        'side_nav':side_nav,
        'settings':settings,
    }
    return context