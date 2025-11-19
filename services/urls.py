from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.product_list, name='product_list'),
    
    # Товары
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    
    # Категории
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    
    # Теги
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('tags/create/', views.tag_create, name='tag_create'),
    
    # Заказы
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.order_create, name='order_create'),
    
    # Дополнительные страницы
    path('profile/', views.user_profile, name='profile'),
    path('cart/', views.cart_page, name='cart'),
    path('settings/', views.settings_page, name='settings'),
    path('about/', views.about_page, name='about'),
]