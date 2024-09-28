from graphene import ObjectType, String, Schema, List
from graphene_django import DjangoObjectType
import asyncio
from User.schema import Query as UserQuery, Mutation as UserMutation
from Creator.schema import Query as CreatorQuery, Mutation as CreatorMutation
from Content.schema import Query as ContentQuery, Mutation as ContentMutation
from Common.schema import Query as CommonQuery, Mutation as CommonMutation

from Api.subscriptions import Subscription as ApiSubscription, MySubscription


class Query(UserQuery, CreatorQuery, ContentQuery, CommonQuery):
    hello = String(name=String(default_value="stranger"))
    yellow = List(String)

    def resolve_hello(self, info, name):
        i = 0
        while i < 200:
            i += 1
            MySubscription.broadcast(group="my_subscription", payload={"value": i})
            asyncio.sleep(1)
        return f"Hello, {name}!"
    
    async def resolve_yellow(self, info):
        i = 0
        while i < 200:
            i += 1
            await MySubscription.broadcast_async(group="my_subscription", payload={"value": f'yellow {i}'})
        return ["yellow"]

class Mutation(UserMutation, CreatorMutation, ContentMutation, CommonMutation):
    pass

class Subscription(ApiSubscription):
    """Root GraphQL subscription."""
    pass

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)