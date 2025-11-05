from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('profile/', views.user_profile, name='profile'),
    path('cart/', views.cart_page, name='cart'),
    path('settings/', views.settings_page, name='settings'),
    path('about/', views.about_page, name='about'),
]