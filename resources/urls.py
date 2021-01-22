from django.contrib import admin
from django.urls import path
from .views import ResourceViewSet
from .views import AlertViewSet

urlpatterns = [
    path('resources', ResourceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('resources/<str:pk>', ResourceViewSet.as_view({
        'get': 'retrieve',
        'put': 'create'
    })),
    path('alerts', AlertViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('alerts/<str:pk>', AlertViewSet.as_view({
        'get': 'retrieve',
        'put': 'create'
    }))
]