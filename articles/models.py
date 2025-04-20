from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
   
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True) 

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    snippet = models.CharField(max_length=200, default="Описание статьи")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated_date', '-created_date']
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"id": self.id})