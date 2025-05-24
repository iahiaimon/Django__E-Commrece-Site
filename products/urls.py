from django.urls import path
from . import views


urlpatterns = [
    path('' , views.home , name="home"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),

    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product_details/<slug:slug>/' , views.product_details , name="product_details"),

]