from django.urls import path
from home.views import *
# urls.py
urlpatterns = [
    # PAGES
    path("",index,name='index'),
    path("search/<str:search>",search,name='search'),
    path("add-to-cart/<str:id>/<str:size>/<str:qty>",add_to_cart,name='add-to-cart'),
    path("remove-item/<str:id>",remove_item,name='remove-item'),
    path("decrease-quantity/<str:id>",decrease_quantity,name='decrease-quantity'),
    path("increase-quantity/<str:id>",increase_quantity,name='increase-quantity'),
    path("categories",categories,name='categories'),
    path("cart",cart,name='cart'),
    path("create-order",create_order,name='create-order'),
    path('payment-verification/', payment_verification, name='payment_verification'),
    path("my-orders",my_orders,name='my-orders'),
    path("track-order/<str:id>",track_order,name='track-order'),
    path("save-address",save_address,name='save-address'),
    path("search_suggestions",search_suggestions,name='search_suggestions'),
    path("about",about,name='about'),
    path("contact",contact,name='contact'),
    path("disclaimer",disclaimer,name='disclaimer'),
    path("termsofuse",termsofuse,name='termsofuse'),
    path("privacypolicy",privacypolicy,name='privacypolicy'),
    path("refundpolicy",refundpolicy,name='refundpolicy'),
    path("contact",contact,name='contact'),
    path('<slug:slug>',product_view, name='product-view'),
]