import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Content.models import Story, Post, PostPoll, PostImage, PostPollVote
from Api import relay
from Creator.models import Creator
from nanoid import generate
from Content.types import StoryUpdateInput, PostInput, PostPollOptionInput, PostPollOptionObject
from Common.models import Category, Tag
from datetime import datetime
from User.Utils.tools import ImageHandler
from Common.types import ImageInput


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
            'text': ['exact', 'icontains'],
            'key': ['exact'],
        }
        fields = '__all__'
        use_connection = True

class PostPollObject(DjangoObjectType):
    class Meta:
        model = PostPoll
        interfaces = (relay.Node, )
        filter_fields = {
            'question': ['exact', 'icontains'],
            'id': ['exact'],
        }
        fields = '__all__'
        use_connection = True

    options = graphene.List(PostPollOptionObject)
    my_vote = graphene.Int()
    votes_count = graphene.Int()

    def resolve_options(self, info):
        if info.context.user:
            votes, count = self.get_votes()
            options = []
            for option in self.options:
                options.append({
                    'id': option.get('id'),
                    'text': option.get('text'),
                    'votes': votes.filter(option=option.get('id')).count()
                })
            return options
        else: self.options

    def resolve_my_vote(self, info):
        if info.context.user:
            id = self.user_vote(info.context.user)
            return id
        return None
    
    def resolve_votes_count(self, info):
        votes, count = self.get_votes()
        return count


class PostImageObject(DjangoObjectType):
    class Meta:
        model = PostImage
        interfaces = (relay.Node, )
        filter_fields = {
            'caption': ['exact', 'icontains'],
            'id': ['exact'],
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
        story.state = data.state.value if data.get('state', None) else story.state
        if data.get('do_publish', False): 
            story.published_at = datetime.now()
            story.state = 'published'
        story.privacy = data.privacy.value if data.get('privacy', None) else story.privacy
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
    
    def mutate(self, info, author_key, data):
        user = info.context.user
        author = Creator.objects.get(key=author_key, user=user)
        if not user and author: raise KeyError('A valid Author is required.')
        type_of = data.type_of.value if data.get('type_of', None) else 'text'
        post = Post(
            author=author,
            text=data.get('text', ''),
            state = data.state.value if data.get('state', None) else 'draft',
            privacy = data.privacy.value if data.get('privacy', None) else 'public',
            published_at = datetime.now(),
            type_of = type_of,
        )
        if data.get('tags', False):
            for tag in data.get('tags'):
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
        if type_of != 'text':
            type_of_id = data.get('type_of_id', None)
            if not type_of_id: raise KeyError('Type of Content Identifier is required.')
            if type_of == 'poll':
                poll = PostPoll.objects.get(id=type_of_id)
                if not poll: raise KeyError('Poll not found.')
                post.type_poll = poll
            elif type_of == 'image':
                image = PostImage.objects.get(id=type_of_id)
                if not image: raise KeyError('Image not found.')
                post.type_image = image
        post.save()
        return CreatePost(post=post)
    
class CreatePostPoll(graphene.Mutation):
    '''Create a new Poll Post'''
    class Input():
        question = graphene.String(required=True)
        options = graphene.List(PostPollOptionInput)

    poll = graphene.Field(PostPollObject)
    
    def mutate(self, info, question, options):
        user = info.context.user
        if not user: raise KeyError('You are not authorized to create a Poll.')
        poll = PostPoll(
            question=question,
            options=options,        
        )
        poll.save()
        return CreatePostPoll(poll=poll)
    
class VotePostPoll(graphene.Mutation):
    '''Vote on a Poll Post'''

    class Input():
        post_key = graphene.String(required=True)
        option_id = graphene.Int(required=True)

    poll = graphene.Field(PostPollObject)
    
    def mutate(self, info, post_key, option_id):
        user = info.context.user
        if not user:
            raise KeyError('You are not authorized to vote on a Poll.')
        
        post = Post.objects.get(key=post_key)
        if not post:
            raise KeyError('Post not found.')
        
        poll = post.type_poll
        if not poll:
            raise KeyError('Poll not found.')
        
        option = poll.option_by_id(option_id)
        if not option:
            raise KeyError('Option not found.')
        userVotes = PostPollVote.objects.filter(user=user, poll=poll)
        is_current_vote = userVotes.filter(option=option_id)
        if is_current_vote.exists():
            is_current_vote.delete()
        else:
            userVotes.delete()
            vote = PostPollVote(user=user, poll=poll, option=option.get('id'))
            vote.save()
        return VotePostPoll(poll=poll)
    
class CreatePostImage(graphene.Mutation):
    '''Create a new Image Post'''
    class Input():
        caption = graphene.String()
        images = graphene.List(ImageInput, required=True)

    post_image = graphene.Field(PostImageObject)
    
    def mutate(self, info, caption, images):
        user = info.context.user
        if not user: raise KeyError('You are not authorized to create an Image Post.')
        post_image = PostImage(
            caption=caption,
        )
        for image in images:
            image = ImageHandler(image_input=image).auto_image()
            if image: post_image.images.add(image)
        post_image.save()
        return CreatePostImage(post_image=post_image)


'''****************** QUERIES ******************'''

class Query(graphene.ObjectType):
    Stories = DjangoFilterConnectionField(StoryObject)
    Story = graphene.relay.node.Field(StoryObject)
    Posts = DjangoFilterConnectionField(PostObject)
    Post = graphene.relay.node.Field(PostObject)

    '''***** Non Usefull Queries *****'''
    Polls = DjangoFilterConnectionField(PostPollObject)
    PostImages = DjangoFilterConnectionField(PostImageObject)

'''****************** MUTATIONS ******************'''

class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
    create_post = CreatePost.Field()
    create_post_poll = CreatePostPoll.Field()
    create_post_image = CreatePostImage.Field()
    do_vote_post_poll = VotePostPoll.Field()