from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('product/', views.product_list, name='product_list'),
    path('products/', lambda request: redirect('product_list', permanent=True)),
    path('product/<slug:slug>/', views.product_details, name='product_details'),
]
