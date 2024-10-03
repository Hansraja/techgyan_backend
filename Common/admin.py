from django.contrib import admin
from .models import Image, Category, Tag

# Register your models here.
@admin.register(Image)
class ImageModel(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryModel(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagModel(admin.ModelAdmin):
    pass
