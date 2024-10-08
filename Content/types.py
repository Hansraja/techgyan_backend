from random import choices
import graphene
from Common.types import ImageInput
from django_filters import OrderingFilter, FilterSet
import django_filters
from Content.models import PostComment, StoryComment

class StateEnum(graphene.Enum):
    '''State of the content'''
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    DELETED = 'deleted'

class PrivacyEnum(graphene.Enum):
    '''Privacy of the content'''
    PUBLIC = 'public'
    PRIVATE = 'private'
    UNLISTED = 'unlisted'

class BaseContentInput():
    '''Base Input for Content'''
    tags = graphene.List(graphene.String)
    state = StateEnum()
    privacy = PrivacyEnum()


class StoryUpdateInput(graphene.InputObjectType, BaseContentInput): 
    '''Input for Updating a Story'''
    title = graphene.String()
    content = graphene.String()
    slug = graphene.String()
    description = graphene.String()
    image = ImageInput()
    do_publish = graphene.Boolean()
    category = graphene.String()


'''****************** POST TYPES ******************'''

class PostTypeEnum(graphene.Enum):
    '''Type of Post'''
    TEXT = 'text'
    POLL = 'poll'
    IMAGE = 'image'

class PostImageInput(graphene.InputObjectType):
    image = graphene.List(ImageInput)
    caption = graphene.String()

class PostInput(graphene.InputObjectType, BaseContentInput):
    type_of = PostTypeEnum(required=True)
    type_of_id = graphene.String(description='Type of Content Identifier')
    text = graphene.String()

class PostPollOptionInput(graphene.InputObjectType):
    id = graphene.Int()
    text = graphene.String()

class PostPollOptionObject(graphene.ObjectType):
    id = graphene.Int()
    text = graphene.String()
    votes = graphene.Int()


'''****************** FilterSet  ******************'''

class StoryCommentFilter(FilterSet):
    '''FilterSet for Comment'''
    class Meta:
        model = StoryComment
        fields = {
            'content': ['exact', 'icontains'],
            'id': ['exact'],
            'user__username': ['exact', 'icontains'],
            'user__key': ['exact'],
            'story__key': ['exact'],
            'author__key': ['exact'],
            'parent__id': ['exact'],
        }

    order_by = OrderingFilter(
        choices=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': 'created_at (default)',
            'updated_at': 'updated_at (default)',
        },
    )

class PostCommentFilter(FilterSet):
    '''FilterSet for Post Comment'''
    class Meta:
        model = PostComment
        fields = {
            'content': ['exact', 'icontains'],
            'id': ['exact'],
            'user__username': ['exact', 'icontains'],
            'user__key': ['exact'],
            'post__key': ['exact'],
            'author__key': ['exact'],
            'parent__id': ['exact'],
        }

    order_by = OrderingFilter(
        choices=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': 'created_at (default)',
            'updated_at': 'updated_at (default)',
        }
    )