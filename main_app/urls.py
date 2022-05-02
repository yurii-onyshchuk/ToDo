"""ToDo URL Configuration

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
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:pk>/setting/', views.UserSetting.as_view(), name='setting'),
    path('change_password/', views.ChangePassword.as_view(), name='change-password'),

    path('', views.TaskList.as_view(), name='tasks'),
    path('category/<int:pk>/', views.TaskByCategory.as_view(), name='task-by-category'),
    path('performed/', views.PerformedTask.as_view(), name='performed-task'),
    path('search/', views.SearchList.as_view(), name='search'),

    path('add_task/', views.AddTask.as_view(), name='add-task'),
    path('perform_task/<int:pk>/', views.perform_task, name='perform-task'),
    path('update_task/<int:pk>/', views.UpdateTask.as_view(), name='edit-task'),
    path('delete_task/<int:pk>/', views.DeleteTask.as_view(), name='delete-task'),
    path('recovery_task/<int:pk>/', views.recovery_task, name='recovery-task'),

    path('add_category/', views.AddCategory.as_view(), name='add-category'),
    path('update_category/<int:pk>/', views.UpdateCategory.as_view(), name='update-category'),
    path('delete_category/<int:pk>/', views.DeleteCategory.as_view(), name='delete-category'),

]
