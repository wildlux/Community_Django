from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_po, name='upload_po'),
    path('login/<str:token>/', views.telegram_login, name='telegram_login'),
]