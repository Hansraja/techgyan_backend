import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Content.models import Story, Post
from Api import relay
from Creator.models import Creator
from nanoid import generate
from Content.types import StoryUpdateInput, PostInput
from Common.models import Category, Tag
from datetime import datetime
from User.Utils.tools import ImageHandler


class StoryObject(DjangoObjectType):
    class Meta:
        model = Story
        interfaces = (relay.Node, )
        filter_fields = {
            'title': ['exact', 'icontains'],
            'slug': ['exact', 'icontains'],
            'key': ['exact'],
        }
        fields = '__all__'
        use_connection = True


class PostObject(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node, )
        filter_fields = {
            'title': ['exact', 'icontains'],
            'key': ['exact'],
        }
        fields = '__all__'
        use_connection = True


'''****************** MUTATIONS TYPES ******************'''

class CreateStory(graphene.Mutation):
    '''Create a new Story'''
    class Input():
        author_key = graphene.String(required=True)
        title = graphene.String()
        slug = graphene.String()

    story = graphene.Field(StoryObject)
    
    def mutate(self, info, **args):
        user = info.context.user
        author = Creator.objects.get(key=args.get('author_key'), user=user)
        if not user and author: raise KeyError('A valid Author is required.')
        story = Story(author=author, slug=args.get('slug', generate(size=60)), title=args.get('title', ''), content='')
        story.save()
        return CreateStory(story=story)
    
class UpdateStory(graphene.Mutation):
    '''Update an existing Story'''
    class Input():
        key = graphene.String(required=True)
        data = StoryUpdateInput(required=True)

    story = graphene.Field(StoryObject)
    
    def mutate(self, info, key, data):
        user = info.context.user
        story = Story.objects.get(key=key)
        if not user and story.author.user != user: raise KeyError('A valid Author is required.')
        story.title = data.get('title', story.title)
        story.slug = data.get('slug', story.slug)
        story.content = data.get('content', story.content)
        story.description = data.get('description', story.description)
        if data.get('image', False):
            image = ImageHandler(image_input=data.get('image')).auto_image()
            if image: story.image = image
        story.state = data.get('state', story.state)
        if data.get('do_publish', False): 
            story.published_at = datetime.now()
            story.state = 'published'
        story.privacy = data.get('privacy', story.privacy)
        if data.get('tags', False):
            for tag in data.get('tags'):
                tag, created = Tag.objects.get_or_create(name=tag)
                story.tags.add(tag)
        if data.get('category', False): 
            category = Category.objects.get(name=data.get('category'))
            story.category = category
        story.save()
        return UpdateStory(story=story)
    
class CreatePost(graphene.Mutation):
    '''Create a new Post'''
    class Input():
        author_key = graphene.String(required=True)
        data = PostInput(required=True)

    post = graphene.Field(PostObject)
    
    def mutate(self, info, key, data):
        user = info.context.user
        author = Creator.objects.get(key, user=user)
        if not user and author: raise KeyError('A valid Author is required.')
        post = Post(author=author, slug=data.get('slug', generate(size=60)), title=data.get('title', ''), content='')
        post.save()
        return CreatePost(post=post)


'''****************** QUERIES ******************'''

class Query(graphene.ObjectType):
    Stories = DjangoFilterConnectionField(StoryObject)
    Story = graphene.relay.node.Field(StoryObject)
    Posts = DjangoFilterConnectionField(PostObject)
    Post = graphene.relay.node.Field(PostObject)

'''****************** MUTATIONS ******************'''

class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
    create_post = CreatePost.Field()