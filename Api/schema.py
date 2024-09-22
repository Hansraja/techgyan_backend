from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
from User.schema import Query as UserQuery, Mutation as UserMutation
from Creator.schema import Query as CreatorQuery


class Query(UserQuery, CreatorQuery):
    pass

class Mutation(UserMutation):
    pass

schema = Schema(query=Query, mutation=Mutation)