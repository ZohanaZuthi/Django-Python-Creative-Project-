from django.db import models

# Create your models here.

from django.db import models


class Article(models.Model):
    title=models.CharField(max_length=255)
    article=models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title

class Highlight(models.Model):
   article=models.ForeignKey(Article, related_name='highlights', on_delete=models.CASCADE)
   slug = models.SlugField(max_length=100)
   text=models.CharField(max_length=255)
   text_content=models.TextField(blank=True, null=True)
   
   image=models.ImageField(upload_to='highlights/', blank=True, null=True)
   audio=models.FileField(upload_to='highlights/', blank=True, null=True)
   video=models.FileField(upload_to='highlights/', blank=True, null=True)
   url_link=models.URLField(blank=True, null=True)
   external_link=models.URLField(blank=True, null=True)
   
   def __str__(self):
         return self.text
   class Meta:
        unique_together = ('article', 'slug')
    
    