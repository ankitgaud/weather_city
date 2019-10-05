from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'), #the path for our index view
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('delete/<city_name>', views.delete_city, name='delete'),    

]