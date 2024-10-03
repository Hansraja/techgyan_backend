from django.contrib import admin
from .models import Story, StoryClap, StoryComment, StoryCommentVote

# Register your models here.

@admin.register(Story)
class StoryModel(admin.ModelAdmin):
    pass

@admin.register(StoryClap)
class StoryClapModel(admin.ModelAdmin):
    pass

@admin.register(StoryComment)
class StoryCommentModel(admin.ModelAdmin):
    pass

@admin.register(StoryCommentVote)
class StoryCommentVoteModel(admin.ModelAdmin):
    pass

from .models import Post, PostClap, PostComment, PostCommentVote, PostPoll, PostPollVote, PostImage, PostImageObj

@admin.register(Post)
class PostModel(admin.ModelAdmin):
    pass

@admin.register(PostClap)
class PostClapModel(admin.ModelAdmin):
    pass

@admin.register(PostComment)
class PostCommentModel(admin.ModelAdmin):
    pass

@admin.register(PostCommentVote)
class PostCommentVoteModel(admin.ModelAdmin):
    pass

@admin.register(PostPoll)
class PostPollModel(admin.ModelAdmin):
    pass

@admin.register(PostPollVote)
class PostPollVoteModel(admin.ModelAdmin):
    pass

@admin.register(PostImage)
class PostImageModel(admin.ModelAdmin):
    pass

@admin.register(PostImageObj)
class PostImageObjModel(admin.ModelAdmin):
    pass










