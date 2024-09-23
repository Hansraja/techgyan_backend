from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
from User.schema import Query as UserQuery, Mutation as UserMutation
from Creator.schema import Query as CreatorQuery
from Api.subscriptions import Subscription as ApiSubscription


class Query(UserQuery, CreatorQuery):
    pass

class Mutation(UserMutation):
    pass

class Subscription(ApiSubscription):
    """Root GraphQL subscription."""
    pass

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)