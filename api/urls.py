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
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tasks', views.TaskAPIViewSet, basename='tasks')
router.register('categories', views.CategoriesAPIViewSet, basename='categories')
router.register('users', views.UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/category/<int:pk>/', views.TaskByCategoryAPIView.as_view()),
    path('v1/performed/', views.PerformedTaskAPIView.as_view()),
]