import graphene

class SocialLinkInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()

class ImageInput(graphene.InputObjectType):
    url = graphene.String(required=True)
    provider = graphene.String(required=True)
    alt = graphene.String()
    caption  = graphene.String()