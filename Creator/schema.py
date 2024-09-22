from Creator.models import Creator, CreatorFollower
from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
from User.schema import UserType

class Creator(DjangoObjectType):
    class Meta:
        model = Creator
        fields = "__all__"

class CreatorFollowerType(DjangoObjectType):
    class Meta:
        model = CreatorFollower
        fields = "__all__"

class Query(ObjectType):
    Creators = List(Creator)
    Creator = List(Creator, name=String(), handle=String())
    CreatorFollowers = List(CreatorFollowerType)

    def resolve_Creators(self, info):
        return Creator.objects.all()
    
    def resolve_Creator(self, info, key=None, handle=None):
        if not key and not handle:
            raise Exception('Please provide either name or handle')
        c = Creator.objects.get(key=key) if key else Creator.objects.get(handle=handle)
        return c

    def resolve_CreatorFollowers(self, info):
        return CreatorFollower.objects.all()