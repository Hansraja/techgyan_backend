from urllib.parse import quote_plus
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Common.schema import ImageObject
from Content.models import Story, Post, PostPoll, PostImage, PostPollVote, StoryComment, StoryCommentVote, PostComment, PostCommentVote, StoryClap, PostClap
from Api import relay
from Creator.models import Creator
from nanoid import generate
from Content.types import PostCommentFilter, StoryCommentFilter, StoryUpdateInput, PostInput, PostPollOptionInput, PostPollOptionObject
from Common.models import Category, Tag
from datetime import datetime
from User.Utils.tools import ImageHandler
from Common.types import ImageInput
from django.db import router


class StoryObject(DjangoObjectType):
    class Meta:
        model = Story
        interfaces = (relay.Node, )
        filter_fields = {
            'title': ['exact', 'icontains'],
            'slug': ['exact', 'icontains'],
            'key': ['exact'],
            'state': ['exact'],
            'privacy': ['exact'],
            'author__key': ['exact'],
            'author__handle': ['exact', 'icontains'],
            'author__user__username': ['exact', 'icontains'],
            'author__user__key': ['exact'],
            'category__name': ['exact'],
        }
        fields = '__all__'
        use_connection = True

    comments_count = graphene.Int()
    claps_count = graphene.Int()
    clapped_by_me = graphene.Boolean()
    saved_by_me = graphene.Boolean()

    def resolve_comments_count(self, info):
        return self.comments.filter(parent=None).count()
    
    def resolve_claps_count(self, info):
        return self.claps.count()
    
    def resolve_clapped_by_me(self, info):
        if info.context.user.is_authenticated:
            return self.claps.filter(user=info.context.user).exists()
        else: return False

    def resolve_saved_by_me(self, info):
        if info.context.user.is_authenticated:
            return info.context.user.saved_stories.filter(key=self.key).exists()
        else: return False

    def resolve_image(self, info):
        if self.image: return self.image
        else: return ImageObject(url=f'https://placehold.co/1280x720/pink/black?text={quote_plus(self.title)}')


class StoryClapObject(DjangoObjectType):
    class Meta:
        model = StoryClap
        interfaces = (relay.Node, )
        filter_fields = {
            'id': ['exact'],
        }
        fields = '__all__'
        use_connection = True

class StoryCommentObject(DjangoObjectType):
    class Meta:
        model = StoryComment
        interfaces = (relay.Node, )
        filterset_class = StoryCommentFilter
        fields = '__all__'
        use_connection = True

    votes = graphene.Int()
    my_vote = graphene.String()
    reply_count = graphene.Int()

    def resolve_votes(self, info):
        return self.get_votes()
    
    def resolve_my_vote(self, info):
        if info.context.user.is_authenticated:
            return self.user_vote(info.context.user)
        else: return None

    def resolve_reply_count(self, info):
        return self.replies.count()

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        if info.variable_values.get('parent_Id', None):
            p_Id = info.variable_values.get('parent_Id')
            return queryset.filter(parent__id=p_Id)
        return queryset.filter(parent__id=None)

class PostObject(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node, )
        filter_fields = {
            'text': ['exact', 'icontains'],
            'key': ['exact'],
            'state': ['exact'],
            'privacy': ['exact'],
            'author__key': ['exact'],
            'author__handle': ['exact', 'icontains'],
            'author__user__username': ['exact', 'icontains'],
            'author__user__key': ['exact'],
            'type_of': ['exact'],
            'type_poll__id': ['exact'],
            'type_image__id': ['exact'],
        }
        fields = '__all__'
        use_connection = True

    comments_count = graphene.Int()
    claps_count = graphene.Int()
    clapped_by_me = graphene.Boolean()
    saved_by_me = graphene.Boolean()

    def resolve_comments_count(self, info):
        return self.comments.filter(parent=None).count()
    
    def resolve_claps_count(self, info):
        return self.claps.count()
    
    def resolve_clapped_by_me(self, info):
        if info.context.user.is_authenticated:
            return self.claps.filter(user=info.context.user).exists()
        else: return False

    def resolve_saved_by_me(self, info):
        if info.context.user.is_authenticated:
            return info.context.user.saved_posts.filter(key=self.key).exists()
        else: return False

class PostClapObject(DjangoObjectType):
    class Meta:
        model = PostClap
        interfaces = (relay.Node, )
        filter_fields = {
            'id': ['exact'],
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
        if info.context.user.is_authenticated:
            votes, count = self.get_votes()
            options = []
            for option in self.options:
                options.append({
                    'id': option.get('id'),
                    'text': option.get('text'),
                    'votes': votes.filter(option=option.get('id')).count()
                })
            return options
        else: return self.options

    def resolve_my_vote(self, info):
        if info.context.user.is_authenticated:
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

class PostCommentObject(DjangoObjectType):
    class Meta:
        model = PostComment
        interfaces = (relay.Node, )
        filterset_class = PostCommentFilter
        fields = '__all__'
        use_connection = True

    votes = graphene.Int()
    my_vote = graphene.String()
    reply_count = graphene.Int()

    def resolve_votes(self, info):
        return self.get_votes()
    
    def resolve_my_vote(self, info):
        if info.context.user.is_authenticated:
            return self.user_vote(info.context.user)
        else: return None

    def resolve_reply_count(self, info):
        return self.replies.count()

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        if info.variable_values.get('parent_Id', None):
            p_Id = info.variable_values.get('parent_Id')
            return queryset.filter(parent__id=p_Id)
        return queryset.filter(parent__id=None)
    

'''****************** MUTATIONS TYPES ******************'''

class CreateStory(graphene.Mutation):
    '''Create a new Story'''
    class Input():
        author_key = graphene.String(required=True)
        title = graphene.String()
        slug = graphene.String()

    story = graphene.Field(StoryObject)
    
    def mutate(self, info, **args):
        user = info.context.user if info.context.user.is_authenticated else None
        author = Creator.objects.get(key=args.get('author_key'), user=user)
        if not user and author: raise Exception('A valid Author is required.')
        story = Story(author=author, slug=args.get('slug', generate(size=60)), title=args.get('title', ''), content='')
        story.save()
        return CreateStory(story=story)

class StoryClapAction(graphene.Mutation):
    '''Clap on a Story'''
    class Input():
        story_key = graphene.String(required=True)

    story = graphene.Field(StoryObject)
    
    def mutate(self, info, story_key):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to clap on a Story.')
        story = Story.objects.get(key=story_key)
        if not story: raise Exception('Story not found.')
        clap = StoryClap.objects.filter(user=user, story=story)
        if clap.exists():
            clap.delete()
            story.refresh_from_db()
            return StoryClapAction(story=story)
        clap = StoryClap(user=user, story=story)
        clap.save()
        story.refresh_from_db()
        return StoryClapAction(story=story)
    
class saveStoryAction(graphene.Mutation):
    '''Save a Story'''
    class Input():
        story_key = graphene.String(required=True)

    story = graphene.Field(StoryObject)
    success = graphene.Boolean(default_value=False)
    
    def mutate(self, info, story_key):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to save a Story.')
        story = Story.objects.get(key=story_key)
        if not story: raise Exception('Story not found.')
        if user.saved_stories.filter(key=story_key).exists():
            user.saved_stories.remove(story)
            return saveStoryAction(story=story, success=True)
        user.saved_stories.add(story)
        return saveStoryAction(story=story, success=True)
    
class UpdateStory(graphene.Mutation):
    '''Update an existing Story'''
    class Input():
        key = graphene.String(required=True)
        data = StoryUpdateInput(required=True)

    story = graphene.Field(StoryObject)
    
    def mutate(self, info, key, data):
        user = info.context.user if info.context.user.is_authenticated else None
        story = Story.objects.get(key=key)
        if not user and story.author.user != user: raise Exception('A valid Author is required.')
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
    
class CreateStoryComment(graphene.Mutation):
    '''Create a new Comment on a Story'''
    class Input():
        story_key = graphene.String(required=True)
        text = graphene.String(required=True)
        parent_id = graphene.String()
        author_key = graphene.String()

    comment = graphene.Field(StoryCommentObject)
    
    def mutate(self, info, story_key, text, parent_id=None, author_key=None):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to comment on a Story.')
        story = Story.objects.get(key=story_key)
        if not story: raise Exception('Story not found.')
        author = None
        if author_key:
            author = Creator.objects.get(key=author_key, user=user)
            if not author: raise Exception('Author not found.')
        parent = StoryComment.objects.get(id=parent_id) if parent_id else None
        comment = StoryComment(
            user = user,
            story=story,
            content=text,
            author=author,
            parent=parent,
        )
        comment.save()
        return CreateStoryComment(comment=comment)
    
class UpdateStoryComment(graphene.Mutation):    
    '''Update an existing Comment on a Story'''
    class Input():
        comment_id = graphene.String(required=True)
        text = graphene.String(required=True)

    comment = graphene.Field(StoryCommentObject)
    
    def mutate(self, info, comment_id, text):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to update a Comment.')
        comment = StoryComment.objects.get(id=comment_id)
        if not comment: raise Exception('Comment not found.')
        if comment.user != user: raise Exception('You are not authorized to update this Comment.')   
        comment.content = text
        comment.updated_at = datetime.now()
        comment.save()
        return UpdateStoryComment(comment=comment)
    
class StoryCommentVoteAction(graphene.Mutation):
    '''Vote on a Comment'''
    class Input():
        comment_id = graphene.String(required=True)

    comment = graphene.Field(StoryCommentObject)
    
    def mutate(self, info, comment_id):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to vote on a Comment.')
        comment = StoryComment.objects.get(id=comment_id)
        if not comment: raise Exception('Comment not found.')
        vote = StoryCommentVote.objects.filter(user=user, comment=comment)
        if vote.exists():
            vote.delete()
        else:
            vote = StoryCommentVote(user=user, comment=comment)
            vote.save()
        return StoryCommentVoteAction(comment=comment)
    
class CreatePost(graphene.Mutation):
    '''Create a new Post'''
    class Input():
        author_key = graphene.String(required=True)
        data = PostInput(required=True)

    post = graphene.Field(PostObject)
    
    def mutate(self, info, author_key, data):
        user = info.context.user if info.context.user.is_authenticated else None
        author = Creator.objects.get(key=author_key, user=user)
        if not user and author: raise Exception('A valid Author is required.')
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
            if not type_of_id: raise Exception('Type of Content Identifier is required.')
            if type_of == 'poll':
                poll = PostPoll.objects.get(id=type_of_id)
                if not poll: raise Exception('Poll not found.')
                post.type_poll = poll
            elif type_of == 'image':
                image = PostImage.objects.get(id=type_of_id)
                if not image: raise Exception('Image not found.')
                post.type_image = image
        post.save()
        return CreatePost(post=post)
    
class UpdatePost(graphene.Mutation):

    class Input():
        key = graphene.String(required=True)
        text = graphene.String(required=True)

    post = graphene.Field(PostObject)
    
    def mutate(self, info, key, text):
        user = info.context.user if info.context.user.is_authenticated else None
        post = Post.objects.get(key=key, user=user)
        if not user and post: raise Exception('Post not found.')
        post.text = text
        post.save()
        return UpdatePost(post=post)
    
class savePostAction(graphene.Mutation):
    '''Save a Post'''
    class Input():
        post_key = graphene.String(required=True)

    post = graphene.Field(PostObject)
    success = graphene.Boolean(default_value=False)
    
    def mutate(self, info, post_key):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to save a Post.')
        post = Post.objects.get(key=post_key)
        if not post: raise Exception('Post not found.')
        if user.saved_posts.filter(key=post_key).exists():
            user.saved_posts.remove(post)
            return savePostAction(post=post, success=True)
        user.saved_posts.add(post)
        return savePostAction(post=post, success=True)
    
class PostClapAction(graphene.Mutation):
    '''Clap on a Post'''
    class Input():
        post_key = graphene.String(required=True)

    post = graphene.Field(PostObject)
    
    def mutate(self, info, post_key):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to clap on a Post.')
        post = Post.objects.get(key=post_key)
        if not post: raise Exception('Post not found.')
        clap = PostClap.objects.filter(user=user, post=post)
        if clap.exists():
            clap.delete()
            post.refresh_from_db()
            return PostClapAction(post=post)
        clap = PostClap(user=user, post=post)
        clap.save()
        post.refresh_from_db()
        return PostClapAction(post=post)
    
class CreatePostPoll(graphene.Mutation):
    '''Create a new Poll Post'''
    class Input():
        question = graphene.String(required=True)
        options = graphene.List(PostPollOptionInput)

    poll = graphene.Field(PostPollObject)
    
    def mutate(self, info, question, options):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to create a Poll.')
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
        user = info.context.user if info.context.user.is_authenticated else None
        if not user:
            raise Exception('You are not authorized to vote on a Poll.')
        
        post = Post.objects.get(key=post_key)
        if not post:
            raise Exception('Post not found.')
        
        poll = post.type_poll
        if not poll:
            raise Exception('Poll not found.')
        
        option = poll.option_by_id(option_id)
        if not option:
            raise Exception('Option not found.')
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
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to create an Image Post.')
        db = router.db_for_write(PostImage)
        post_image = PostImage.objects.using(db).create(
            caption=caption,
        )
        for image in images:
            image = ImageHandler(image_input=image).auto_image()
            if image: post_image.images.add(image)
        post_image.save(using=db)
        return CreatePostImage(post_image=post_image)
    
class CreatePostComment(graphene.Mutation):
    '''Create a new Comment on a Post'''
    class Input():
        post_key = graphene.String(required=True)
        text = graphene.String(required=True)
        parent_id = graphene.String()
        author_key = graphene.String()

    comment = graphene.Field(PostCommentObject)
    
    def mutate(self, info, post_key, text, parent_id=None, author_key=None):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to comment on a Post.')
        post = Post.objects.get(key=post_key)
        if not post: raise Exception('Post not found.')
        author = None
        if author_key:
            author = Creator.objects.get(key=author_key, user=user)
            if not author: raise Exception('Author not found.')
        parent = PostComment.objects.get(id=parent_id) if parent_id else None
        comment = PostComment(
            user = user,
            post=post,
            content=text,
            author=author,
            parent=parent,
        )
        comment.save()
        return CreatePostComment(comment=comment)
    
class UpdatePostComment(graphene.Mutation):
    '''Update an existing Comment on a Post'''
    class Input():
        comment_id = graphene.String(required=True)
        text = graphene.String(required=True)

    comment = graphene.Field(PostCommentObject)
    
    def mutate(self, info, comment_id, text):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to update a Comment.')
        comment = PostComment.objects.get(id=comment_id)
        if not comment: raise Exception('Comment not found.')
        if comment.user != user: raise Exception('You are not authorized to update this Comment.')   
        comment.content = text
        comment.updated_at = datetime.now()
        comment.save()
        return UpdatePostComment(comment=comment)

class PostCommentVoteAction(graphene.Mutation):
    '''Vote on a Comment'''
    class Input():
        comment_id = graphene.String(required=True)

    comment = graphene.Field(PostCommentObject)
    
    def mutate(self, info, comment_id):
        user = info.context.user if info.context.user.is_authenticated else None
        if not user: raise Exception('You are not authorized to vote on a Comment.')
        comment = PostComment.objects.get(id=comment_id)
        if not comment: raise Exception('Comment not found.')
        vote = PostCommentVote.objects.filter(user=user, comment=comment)
        if vote.exists():
            vote.delete()
        else:
            vote = PostCommentVote(user=user, comment=comment)
            vote.save()
        return PostCommentVoteAction(comment=comment)


'''****************** QUERIES ******************'''

class Query(graphene.ObjectType):
    Stories = DjangoFilterConnectionField(StoryObject)
    Story = graphene.relay.node.Field(StoryObject)
    Posts = DjangoFilterConnectionField(PostObject)
    Post = graphene.relay.node.Field(PostObject)
    StoryComments = DjangoFilterConnectionField(StoryCommentObject)
    PostComments = DjangoFilterConnectionField(PostCommentObject)

    '''***** User Content *****'''
    MySavedStories = DjangoFilterConnectionField(StoryObject)

    '''***** Non Usefull Queries *****'''
    Polls = DjangoFilterConnectionField(PostPollObject)
    PostImages = DjangoFilterConnectionField(PostImageObject)

    def resolve_MySavedStories(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user.saved_stories.all()
        return None

'''****************** MUTATIONS ******************'''

class Mutation(graphene.ObjectType):

    '''***** STORY MUTATIONS *****'''
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
    create_story_comment = CreateStoryComment.Field()
    update_story_comment = UpdateStoryComment.Field()
    clap_on_story = StoryClapAction.Field()
    save_story = saveStoryAction.Field()
    vote_on_story_comment = StoryCommentVoteAction.Field()

    '''***** POST MUTATIONS *****'''
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    clap_on_post = PostClapAction.Field()
    save_post = savePostAction.Field()
    create_post_comment = CreatePostComment.Field()
    update_post_comment = UpdatePostComment.Field()
    vote_on_post_comment = PostCommentVoteAction.Field()

    create_post_poll = CreatePostPoll.Field()
    do_vote_post_poll = VotePostPoll.Field()
    create_post_image = CreatePostImage.Field()