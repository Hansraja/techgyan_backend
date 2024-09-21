from django.db import models
from nanoid import generate
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Creator(models.Model):
    key = models.CharField(max_length=24, unique=True, editable=False)
    name = models.CharField(max_length=255)
    handle = models.CharField(max_length=180, unique=True, db_collation="case_insensitive")
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey('Common.Image', on_delete=models.SET_NULL, null=True, blank=True)
    banner = models.ForeignKey('Common.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='banner')
    social = ArrayField(models.JSONField(default=dict), blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'creators'
        verbose_name = 'creator'
        verbose_name_plural = 'creators'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.key = generate(size=24)
        super().save(*args, **kwargs)
        return self
    
class CreatorFollower(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='followers')
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'creator_followers'
        verbose_name = 'creator follower'
        verbose_name_plural = 'creator followers'
    
    def __str__(self):
        return f'{self.creator.name} - {self.user.username}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self