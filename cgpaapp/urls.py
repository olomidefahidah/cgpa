from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calculate/', views.calculate, name='calculate'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('semester/<int:pk>/', views.semester_detail, name='semester_detail'),
]