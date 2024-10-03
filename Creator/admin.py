from django.contrib import admin
from .models import Creator, CreatorFollower
# Register your models here.

@admin.register(Creator)
class CreateorModel(admin.ModelAdmin):
    pass

@admin.register(CreatorFollower)
class CreatorFollower(admin.ModelAdmin):
    pass