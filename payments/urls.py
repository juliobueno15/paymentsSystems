from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('payment/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payment/new', views.payment_new, name='payment_new'),
    path('payment/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('register', views.register, name='register'),
]