import graphene
from graphene_django import DjangoObjectType
from Common.models import Image, Tag, Category
from User.Utils.tools import ImageUrlBuilder

class SocialLinkInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()

class ImageObject(DjangoObjectType):
    public_id = graphene.String()
    class Meta:
        model = Image
        fields = ('url', 'id', 'alt', 'caption', 'provider')

    def resolve_url(self, info):
        return ImageUrlBuilder(self).build_url()
    
    def resolve_public_id(self, info):
        return self.url

class TagObject(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'

class CategoryObject(DjangoObjectType):

    class Meta:
        model = Category
        fields = '__all__'


class Query(graphene.ObjectType):
    Tags = graphene.List(TagObject)
    Categories = graphene.List(CategoryObject)

class Mutation(graphene.ObjectType):
    pass