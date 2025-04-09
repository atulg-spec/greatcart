from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blogs'),
    path('<slug:slug>/',views.blog_page_view, name='blog-page-view'),
]
