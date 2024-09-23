import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Content.models import Story, Post
from Api import relay
from Creator.models import Creator
from nanoid import generate


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

class CreateStory(graphene.Mutation):
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

class Query(graphene.ObjectType):
    Stories = DjangoFilterConnectionField(StoryObject)
    Story = graphene.relay.node.Field(StoryObject)

class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()