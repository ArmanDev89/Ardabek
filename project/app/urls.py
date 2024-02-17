from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('generate', views.generate, name='generate')
]