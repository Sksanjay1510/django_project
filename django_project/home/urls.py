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
    path('signout/', views.signout, name='signout'),
    path('get-started/', views.get_started, name='get_started'),
    path('news/', views.news, name='news'),
    path('partners/', views.partners, name='partners'),
    path('documentation/', views.documentation, name='documentation'),
    path('help-center/', views.help_center, name='help_center'),
    path('status/', views.status, name='status'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
    # User Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Session keep-alive
    path('keep-alive/', views.keep_alive, name='keep_alive'),
    
    # Custom Admin URL
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-contacts/', views.admin_contacts, name='admin_contacts'),
    path('admin-contact/<int:contact_id>/', views.admin_contact_detail, name='admin_contact_detail'),
    path('admin-careers/', views.admin_careers, name='admin_careers'),
    path('admin-applications/', views.admin_applications, name='admin_applications'),
    path('admin-application/<int:application_id>/', views.admin_application_detail, name='admin_application_detail'),
    path('admin-replies/', views.admin_replies, name='admin_replies'),
    path('admin-bulk-actions/', views.admin_bulk_actions, name='admin_bulk_actions'),
    path('admin-testimonials/', views.admin_testimonials, name='admin_testimonials'),
    path('admin-faqs/', views.admin_faqs, name='admin_faqs'),
    path('admin-settings/', views.admin_settings, name='admin_settings'),
]