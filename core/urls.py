
from django.urls import path,include

from .views import Home,DetailItem,Cart,Update_Cart,Remove_from_cart,Coupon_add,Checkout,Billing_Adress,Payment_stripe,Payment_paypal,about_us,contact_us,Your_Orders,Remove_Order


app_name='core'

urlpatterns = [
  path('',Home,name='home'),
  path('about-us/',about_us,name="about_us"),
  path('contact-us/',contact_us,name="contact_us"),
  path('orders/',Your_Orders,name="your_orders"),
  path('detail/<int:pk>/',DetailItem,name='detail_item'),
  path('cart/',Cart,name="cart"),
  path('update/cart/',Update_Cart,name="update_cart"),
  path('remove/fromcart/<int:pk>',Remove_from_cart,name="remove_from_cart"),
  path('remove/order/<int:pk>',Remove_Order,name='remove_order'),
  path('add/coupon/',Coupon_add, name="coupon"),
  path('checkout/',Checkout,name="checkout"),
  path('order/payment/stripe/',Payment_stripe,name="stripe"),
  path('billing_adress/',Billing_Adress,name="adress"),
  path('order/payment/paypal/',Payment_paypal,name="paypal"),
  


]

