# Generated by Django 5.1.1 on 2024-10-03 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Content', '0006_alter_storycomment_story'),
        ('Creator', '0002_creator_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='Creator.creator'),
        ),
        migrations.AlterField(
            model_name='postclap',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claps', to='Content.post'),
        ),
        migrations.AlterField(
            model_name='postclap',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_claps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='Creator.creator'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Content.postcomment'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Content.post'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postcommentvote',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='Content.postcomment'),
        ),
        migrations.AlterField(
            model_name='postpollvote',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='Content.postpoll'),
        ),
        migrations.AlterField(
            model_name='postpollvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='story',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='Creator.creator'),
        ),
        migrations.AlterField(
            model_name='storyclap',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claps', to='Content.story'),
        ),
        migrations.AlterField(
            model_name='storyclap',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_claps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='story_comments', to='Creator.creator'),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Content.storycomment'),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storycommentvote',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='Content.storycomment'),
        ),
    ]
