# Generated by Django 5.1.1 on 2024-09-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.CharField(editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('url', models.CharField(max_length=255)),
                ('alt', models.CharField(blank=True, max_length=255, null=True)),
                ('caption', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider', models.CharField(default='cloudinary', max_length=255)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.CharField(editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'db_table': 'tags',
            },
        ),
    ]
