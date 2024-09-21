from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
from User.schema import Query as UserQuery
from Creator.schema import Query as CreatorQuery


class Query(UserQuery, CreatorQuery):
    pass

schema = Schema(query=Query)