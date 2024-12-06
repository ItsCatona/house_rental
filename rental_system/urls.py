from django.contrib import admin
from django.urls import path
from rental_system import views
from .views import properties_view

from .views import property_detail_view
from .views import  tenant_detail_view
from .views import contact_view

from django.contrib.auth import views as auth_views
from .views import register_view

from .views import (
    create_tenant, edit_tenant, delete_tenant,
    create_property, edit_property, delete_property
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('tenant/<int:tenant_id>/', views.tenant_dashboard, name='tenant_dashboard'),
    path('landlord_dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('', views.starter_page, name='starter_page'),
    path('index', views.index, name='index'),
    path('agents', views.agents, name='agents'),
    path('properties', views.properties_view, name='properties_view'),
    path('property-single', views.property_single, name='property-single'),
    path('properties/', properties_view, name='properties'),

    path('tenants/', views.tenants_view, name='tenants'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('property/<int:property_id>/', property_detail_view, name='property-detail'),

    path('tenant/<int:tenant_id>/', tenant_detail_view, name='tenant-detail'),
    path('contact/', contact_view, name='contact'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),

    # Tenants
    path('tenant/create/', create_tenant, name='create-tenant'),
    path('tenant/<int:tenant_id>/edit/', edit_tenant, name='edit-tenant'),
    path('tenant/<int:tenant_id>/delete/', delete_tenant, name='delete-tenant'),

    # Properties
    path('property/create/', create_property, name='create-property'),
    path('property/<int:property_id>/edit/', edit_property, name='edit-property'),
    path('property/<int:property_id>/delete/', delete_property, name='delete-property'),

]
