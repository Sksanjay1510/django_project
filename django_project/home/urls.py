from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('products/eagle-pro/', views.product_eagle_pro, name='product_eagle_pro'),
    path('products/eagle-mini/', views.product_eagle_mini, name='product_eagle_mini'),
    path('products/sparrow/', views.product_sparrow, name='product_sparrow'),
    path('career/', views.career, name='career'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('get-started/', views.get_started, name='get_started'),
    path('news/', views.news, name='news'),
    path('partners/', views.partners, name='partners'),
    path('documentation/', views.documentation, name='documentation'),
    path('help-center/', views.help_center, name='help_center'),
    path('status/', views.status, name='status'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
    
    # Custom Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-contacts/', views.admin_contacts, name='admin_contacts'),
    path('admin-careers/', views.admin_careers, name='admin_careers'),
    path('admin-applications/', views.admin_applications, name='admin_applications'),
    path('admin-testimonials/', views.admin_testimonials, name='admin_testimonials'),
    path('admin-faqs/', views.admin_faqs, name='admin_faqs'),
    path('admin-settings/', views.admin_settings, name='admin_settings'),
]