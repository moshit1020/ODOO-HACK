from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('trip/new/', views.create_trip, name='create_trip'),
    path('trip/<int:trip_id>/', views.itinerary, name='itinerary'),
    path('trip/<int:trip_id>/add_stop/', views.add_stop, name='add_stop'),
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/cities/', views.admin_city_list, name='admin_city_list'),
    path('admin-panel/cities/new/', views.admin_city_create, name='admin_city_create'),
    path('admin-panel/cities/<int:city_id>/edit/', views.admin_city_edit, name='admin_city_edit'),
    path('admin-panel/cities/<int:city_id>/delete/', views.admin_city_delete, name='admin_city_delete'),
    path('admin-panel/trips/', views.admin_trip_list, name='admin_trip_list'),
    path('admin-panel/trips/<int:trip_id>/delete/', views.admin_trip_delete, name='admin_trip_delete'),
]
