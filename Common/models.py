from django.db import models
from nanoid import generate

# Create your models here.

class Image(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    url = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    provider = models.CharField(max_length=255, default='cloudinary')

    class Meta:
        db_table = 'images'
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
class Tag(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
class Category(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self