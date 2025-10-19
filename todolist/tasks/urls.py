from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import taskviewset

router = DefaultRouter()
router.register(r"tasklist", taskviewset, basename="task")

urlpatterns = [
    path('', include(router.urls)),
]