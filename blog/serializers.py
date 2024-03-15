from rest_framework import serializers 
from blog.models import BlogpostModel,NoticeModel

class BlogpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogpostModel
        fields = '__all__' 

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeModel
        fields = '__all__' 