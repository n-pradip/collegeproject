from django.shortcuts import render
from .serializers import BlogpostSerializer, NoticeSerializer
from blog.models import BlogpostModel,NoticeModel
from rest_framework import viewsets

class BlogpostViewset(viewsets.ModelViewSet):
    queryset = BlogpostModel.objects.all()
    serializer_class = BlogpostSerializer

class NoticeViewset(viewsets.ModelViewSet):
    queryset = NoticeModel.objects.all()
    serializer_class = NoticeSerializer