from django.db import models

class BlogpostModel(models.Model):
    title = models.CharField(max_length=128)
    author=  models.CharField(max_length=128)
    content = models.TextField() 
    image = models.ImageField(upload_to='blogpost_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
 
