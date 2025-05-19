from django.urls import path
from . import views

urlpatterns = [
    path('order_porduct/' , views.order_product , name="order_product")
]