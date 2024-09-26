
from graphene import ObjectType, List, Field, Int, String, relay as gRelay, Boolean
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from Api import relay
from Common.types import ImageInput
from User.Utils.tools import ImageHandler
from User.types import LoginObject
from .models import User

class UserType(DjangoObjectType):
    is_followed = Boolean()
    name = graphene.String()

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')

    def resolve_is_followed(self, info):
        user = info.context.user
        if user.is_anonymous:
            return False
        return self.following.filter(pk=user.pk).exists()
    
    def resolve_name(self, info):
        return self.get_full_name()
    
    def resolve_email(self, info):
        user = info.context.user
        if user.is_anonymous or user.pk != self.pk:
            return None
        return self.email[0] + '*' * (self.email.index('@') - 1) + self.email[self.email.index('@'):]

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

class LoginUser(graphene.Mutation):
    class Arguments:
        email = String()
        password = String()

    user = Field(LoginObject)
    session_id = String()
    success = Boolean()

    def mutate(self, info, email=None, password=None):
        from django.contrib.auth import authenticate, login
        user = authenticate(email=email, password=password)
        if user is None:
            raise Exception('Invalid username or password')
        login(info.context, user)
        return LoginUser(user=user, session_id=info.context.session.session_key, success=True)

class CreateUser(gRelay.ClientIDMutation):
    class Input:
        username = String()
        email = String()
        password = String()

    user = Field(UserType)

    def mutate_and_get_payload(self, info, username = None, email = None, password = None):
        user = User.objects.create_user(username=username, email=email, password=password)
        return CreateUser(user=user)
    
class UserInput(graphene.InputObjectType):
    username = String()
    first_name = String()
    last_name = String()
    sex = String()
    dob = graphene.Date()
    image = ImageInput()

class UpdateUser(graphene.Mutation):
    class Input:
        key = String(required=True)
        data = UserInput()

    user = Field(UserType)

    def mutate(self, info, key = None, data = None):
        user = User.objects.get(key=key)
        user.username = data.username if data.username else user.username
        user.first_name = data.first_name if data.first_name else user.first_name
        user.last_name = data.last_name if data.last_name else user.last_name
        user.sex = data.sex if data.sex else user.sex
        user.dob = data.dob if data.dob else user.dob
        if data.image:
            user.image = ImageHandler(data.image).auto_image()
        user.save()
        return UpdateUser(user=user)
    
class DeleteUser(gRelay.ClientIDMutation):
    class Input:
        username = String()
        key = String()

    user = Field(UserType)

    def mutate_and_get_payload(self, info, username = None, key = None):
        user = User.objects.get(username=username) if username else User.objects.get(key=key)
        user.delete()
        return DeleteUser(user=None)

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login = LoginUser.Field()

class Query(ObjectType):
    Users = DjangoFilterConnectionField(UserNode)
    User = Field(UserType, username=String(), key=String())
    Me = Field(UserType)

    def resolve_User(self, info, username=None, key=None):
        if not username and not key:
            raise Exception('Please provide either username or id')
        u = User.objects.get(username=username) if username else User.objects.get(key=key)
        return u
    
    def resolve_Me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in')
        return user

