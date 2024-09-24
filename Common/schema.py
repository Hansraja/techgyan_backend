import graphene
from graphene_django import DjangoObjectType
from Common.models import Image, Tag, Category
from User.Utils.tools import ImageUrlBuilder

class SocialLinkInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()

class ImageObject(DjangoObjectType):
    class Meta:
        model = Image
        fields = '__all__'

    def resolve_url(self, info):
        return ImageUrlBuilder(self).build_url()

class TagObject(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'

class CategoryObject(DjangoObjectType):

    class Meta:
        model = Category
        fields = '__all__'


class Query(graphene.ObjectType):
    tags = graphene.List(TagObject)
    categories = graphene.List(CategoryObject)

class Mutation(graphene.ObjectType):
    pass