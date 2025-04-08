from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('proceed_payment/<str:orderid>', views.proceed_payment, name='proceed_payment'),
    path('payu_success/', views.payu_success, name='payu_success'),
    path('payu_failure/', views.payu_failure, name='payu_failure'),
    # path('razorpay_callback/', views.razorpay_callback, name='razorpay_callback'),
    path('razorpay/success/', views.razorpay_success, name='razorpay_success'),
    path('razorpay/failure/', views.razorpay_failure, name='razorpay_failure'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
