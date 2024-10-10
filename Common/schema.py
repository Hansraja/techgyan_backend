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
    blur_url = graphene.String()
    has_image = graphene.Boolean()

    class Meta:
        model = Image
        fields = ('url', 'id', 'alt', 'caption', 'provider')

    def resolve_url(self, info):
        if isinstance(self, Image) and self.has_url:
            return self._url
        return ImageUrlBuilder(self).build_url()
    
    def resolve_public_id(self, info):
        return self.url
    
    def resolve_has_image(self, info):
        return self.id is not None
    
    def resolve_blur_url(self, info):
        return 'https://res.cloudinary.com/dxjse9tsv/image/upload/c_fill,g_auto,h_10,w_10/v1629780000/placeholder.jpg'

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

    def resolve_Categories(self, info):
        return Category.objects.all()

class Mutation(graphene.ObjectType):
    pass