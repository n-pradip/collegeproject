from django.urls import path,include
from .views import BlogpostViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'posts', BlogpostViewset, basename='blogpost')

urlpatterns = [
    path('', include(router.urls)),
]