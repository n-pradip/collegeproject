from django.db import models
from django.core.validators import FileExtensionValidator
import uuid



# ============================== Blogpost ==================================
class BlogpostModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=128)
    author=  models.CharField(max_length=128)
    content = models.TextField() 
    image = models.ImageField(upload_to='blogpost_images/')
    video = models.FileField(upload_to='blogpost_videos_upload',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# ============================== Government notice =========================
class NoticeModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=128)
    author=  models.CharField(max_length=128)
    content = models.TextField() 
    image = models.ImageField(upload_to='notice_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title