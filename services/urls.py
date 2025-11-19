from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('tags/', views.tag_list, name='tag_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('categories/create/', views.category_create, name='category_create'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('orders/create/', views.order_create, name='order_create'),
    path('profile/', views.user_profile, name='profile'),
    path('cart/', views.cart_page, name='cart'),
    path('settings/', views.settings_page, name='settings'),
    path('about/', views.about_page, name='about'),
]