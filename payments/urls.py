from django.urls import path
from . import views

urlpatterns = [
    path('place_order/' , views.place_order , name="place_order"),
    path('payment' , views.payment , name="payment"),
    path('order-complete/', views.order_complete, name='order_complete'),
    path("payment_status", views.payment_status, name="payment_status"),
]