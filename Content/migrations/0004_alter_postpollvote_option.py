# Generated by Django 5.1.1 on 2024-09-25 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Content', '0003_alter_postimageobj_options_rename_content_post_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpollvote',
            name='option',
            field=models.IntegerField(),
        ),
    ]
