from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('logout/', views.logout_view, name='logout'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('profile/', views.profile, name='profile'),

    path('checkout/', views.checkout, name='checkout'),

    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    path('my-orders/', views.my_orders, name='my_orders'),

    path('search/', views.search, name='search'),
]


