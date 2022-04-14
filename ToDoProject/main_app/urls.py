"""ToDoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='index'),
    path('add_task', views.add_task, name='add_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    path('perform_task/<int:pk>/', views.perform_task, name='perform_task'),
    path('recovery_task/<int:pk>/', views.recovery_task, name='recovery_task'),
    path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
    path('category/<int:pk>', views.task_by_catagory, name='task_by_category'),
    path('performed_task', views.performed_task, name='performed_task'),
    path('add_category', views.add_category, name='add_category'),
    path('edit_category/<int:pk>', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('search/', views.search, name='search'),
]
