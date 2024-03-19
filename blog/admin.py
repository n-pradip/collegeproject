from django.contrib import admin
from .models import BlogpostModel, NoticeModel

# Register your models here.
admin.site.register(NoticeModel)
admin.site.register(BlogpostModel)