from django.urls import path
from . import views


urlpatterns = [
    path('' , views.home , name="home"),
    # path('cart/' , views.cart_view , name="cart_view"),
    # path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart')

    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product_details/<slug:slug>/' , views.product_details , name="product_details"),


]