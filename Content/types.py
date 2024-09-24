import graphene
from Common.types import ImageInput

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
    title = graphene.String()
    content = graphene.String()
    tags = graphene.List(graphene.String)
    state = StateEnum()
    privacy = PrivacyEnum()


class StoryUpdateInput(graphene.InputObjectType, BaseContentInput):
    slug = graphene.String()
    description = graphene.String()
    image = ImageInput()
    do_publish = graphene.Boolean()
    category = graphene.String()


'''****************** POST TYPES ******************'''

class PollTypeEnum(graphene.Enum):
    '''Type of Poll'''
    TEXT = 'text'
    IMAGE = 'image'

class PostPollInput(graphene.InputObjectType):
    question = graphene.String()
    options = graphene.List(graphene.String)
    correct_option = graphene.Int()
    explanation = graphene.String()

class PostImageInput(graphene.InputObjectType):
    image = graphene.List(ImageInput)
    caption = graphene.String()

class PostContent(graphene.Union):
    class Meta:
        types = (PostPollInput, PostImageInput)

class PostInput(graphene.InputObjectType, BaseContentInput):
    type_of = PollTypeEnum()
    type_of_content = graphene.String()
