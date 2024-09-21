
from graphene import ObjectType, List, Field, Int, String
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Api import relay

from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
        filter_fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'key': ['exact'],
        }
        exclude = ('password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')
        use_connection = True

    # @classmethod
    # def get_node(cls, info, id):
    #     return User.objects.get(pk=id)


class Query(ObjectType):
    Users = List(UserType)
    User = Field(UserType, username=String(), key=String())

    all_users = DjangoFilterConnectionField(UserNode)
    a_user = relay.Node.Field(UserNode)

    def resolve_Users(self, info):
        return User.objects.all()
    
    def resolve_User(self, info, username=None, key=None):
        if not username and not key:
            raise Exception('Please provide either username or id')
        u = User.objects.get(username=username) if username else User.objects.get(key=key)
        return u

