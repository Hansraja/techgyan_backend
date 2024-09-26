import graphene
from User.Utils.tools import ImageUrlBuilder

class LoginObject(graphene.ObjectType):
    username = graphene.String()
    name = graphene.String()
    key = graphene.String()
    image = graphene.String()

    def resolve_name(self, info):
        return self.get_full_name()
    
    def resolve_image(self, info):
        return ImageUrlBuilder(self.image).build_url()
