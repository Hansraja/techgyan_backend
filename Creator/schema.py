import graphene
from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Api import relay
from Common.types import SocialLinkInput, ImageInput
from Creator.models import Creator, CreatorFollower
from Creator.types import CreatorFollowedObject, CreatorNotificationEnum
from User.Utils.tools import ImageHandler
from Common.schema import ImageObject

class CreatorInput(graphene.InputObjectType):
    name = graphene.String()
    handle = graphene.String()
    description = graphene.String()
    social = List(SocialLinkInput)
    contact_email = graphene.String()
    image = ImageInput()
    banner = ImageInput()

class SocialLink(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()

class CreatorObject(DjangoObjectType):
    social = List(SocialLink)
    followed = graphene.Field(CreatorFollowedObject)
    banner = ImageObject()

    class Meta:
        model = Creator
        fields = "__all__"
        interfaces = (relay.Node, )
        use_connection = True
        filter_fields = {
            'name': ['exact', 'icontains'],
            'handle': ['exact', 'icontains'],
            'key': ['exact'],
            'user__key': ['exact'],
            'user__username': ['exact', 'icontains']
        }

    def resolve_followed(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        else:
            data = CreatorFollower.objects.filter(creator=self, user=user).first()
            if not data:
                return CreatorFollowedObject(False, None)
            return CreatorFollowedObject(True, data.notifications)

    def resolve_banner(self, info):
        banner = self.banner
        if not banner:
            return None
        banner.has_url = True
        banner._url = self.get_banner_url()
        return banner

class CreatorFollowerType(DjangoObjectType):
    class Meta:
        model = CreatorFollower
        fields = "__all__"
        interfaces = (relay.Node, )
        use_connection = True
        filter_fields = {
            'creator': ['exact'],
            'user': ['exact']
        }

class CreateCreator(graphene.Mutation):
    class Input:
        name = graphene.String(required=True)
        handle = graphene.String(required=True)

    creator = graphene.Field(CreatorObject)

    def mutate(self, info, name, handle):
        user = info.context.user
        new_creator = Creator(name=name, handle=handle, user=user)
        new_creator.save()
        return CreateCreator(creator=new_creator)
    
class UpdateCreator(graphene.Mutation):
    class Input:
        key = graphene.String(required=True)
        data = CreatorInput(required=True)

    creator = graphene.Field(CreatorObject)

    def mutate(self, info, key, data):
        creator = Creator.objects.get(key=key)
        if data.name: creator.name = data.name
        if data.description: creator.description = data.description
        if data.social: creator.social = data.social
        if data.contact_email: creator.contact_email = data.contact_email
        if data.handle: creator.handle = data.handle
        if data.image:
            creator.image = ImageHandler(data.image).auto_image()
        if data.banner:
            creator.banner = ImageHandler(data.banner).auto_image()
        creator.save()
        return UpdateCreator(creator=creator)
    
class FollowCreator(graphene.Mutation):
    class Input:
        creator_key = graphene.String(required=True)
        notifications = CreatorNotificationEnum()

    creator = graphene.Field(CreatorObject)

    def mutate(self, info, creator_key, notifications):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Please login to follow a creator')
        creator = Creator.objects.get(key=creator_key)
        is_following = CreatorFollower.objects.filter(creator=creator, user=user).first()
        if is_following:
            is_following.notifications = notifications.value
            is_following.save()
            return FollowCreator(creator=creator)
        new_follower = CreatorFollower(creator=creator, user=user, notifications=notifications.value)
        new_follower.save()
        return FollowCreator(creator=creator)


class UnfollowCreator(graphene.Mutation):
    class Input:
        creator_key = graphene.String(required=True)

    creator = graphene.Field(CreatorObject)

    def mutate(self, info, creator_key):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Please login to unfollow a creator')
        creator = Creator.objects.get(key=creator_key)
        is_following = CreatorFollower.objects.filter(creator=creator, user=user)
        if not is_following.exists():
            raise Exception('You are not following this creator')
        is_following.delete()
        return UnfollowCreator(creator=creator)

class Query(ObjectType):
    Creators = DjangoFilterConnectionField(CreatorObject)
    Creator = graphene.Field(CreatorObject, name=String(), handle=String())
    CreatorFollowers = List(CreatorFollowerType)

    def resolve_Creator(self, info, key=None, handle=None):
        if not key and not handle:
            raise Exception('Please provide either key or handle')
        c = Creator.objects.get(key=key) if key else Creator.objects.get(handle=handle)
        return c

    def resolve_CreatorFollowers(self, info):
        return CreatorFollower.objects.all()
    

class Mutation(graphene.ObjectType):
    create_creator = CreateCreator.Field()
    update_creator = UpdateCreator.Field()
    follow_creator = FollowCreator.Field()
    unfollow_creator = UnfollowCreator.Field()