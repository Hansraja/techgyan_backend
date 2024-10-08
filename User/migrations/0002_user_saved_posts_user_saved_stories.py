# Generated by Django 5.1.1 on 2024-10-05 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saved_posts',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='Content.post'),
        ),
        migrations.AddField(
            model_name='user',
            name='saved_stories',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='Content.story'),
        ),
    ]
