from Creator.models import Creator, CreatorFollower
from graphene import ObjectType, String, Schema, List
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from User.schema import UserType
from Api import relay
from Common.types import SocialLinkInput, ImageInput
from Creator.models import Creator as CreatorModel
from User.Utils.tools import ImageHandler

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

class Creator(DjangoObjectType):
    social = List(SocialLink)
    class Meta:
        model = Creator
        fields = "__all__"
        interfaces = (relay.Node, )
        use_connection = True
        filter_fields = {
            'name': ['exact', 'icontains'],
            'handle': ['exact', 'icontains'],
            'key': ['exact']
        }

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

    creator = graphene.Field(Creator)

    def mutate(self, info, name, handle):
        user = info.context.user
        new_creator = CreatorModel(name=name, handle=handle, user=user)
        new_creator.save()
        return CreateCreator(creator=new_creator)
    
class UpdateCreator(graphene.Mutation):
    class Input:
        key = graphene.String(required=True)
        data = CreatorInput(required=True)

    creator = graphene.Field(Creator)

    def mutate(self, info, key, data):
        creator = CreatorModel.objects.get(key=key)
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

class Query(ObjectType):
    Creators = DjangoFilterConnectionField(Creator)
    Creator = graphene.Field(Creator, name=String(), handle=String())
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
