from django.urls import path
from . import views

urlpatterns = [
    path("render/", views.render_ad, name="render_ad"),
]
