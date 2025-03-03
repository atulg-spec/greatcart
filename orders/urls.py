from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('proceed_payment/<str:orderid>', views.proceed_payment, name='proceed_payment'),
    path('payu_success/', views.payu_success, name='payu_success'),
    path('payu_failure/', views.payu_failure, name='payu_failure'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
