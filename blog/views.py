from django.shortcuts import render
from .serializers import BlogpostSerializer
from blog.models import BlogpostModel
from rest_framework import viewsets

class BlogpostViewset(viewsets.ModelViewSet):
    queryset = BlogpostModel.objects.all()
    serializer_class = BlogpostSerializer