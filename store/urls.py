from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:part_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:part_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:part_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('order/confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('track/', views.track_order, name='track_order'),
]