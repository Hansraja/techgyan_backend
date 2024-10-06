
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
    name = graphene.String()

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login')
    
    def resolve_name(self, info):
        return self.get_full_name()
    
    def resolve_email(self, info):
        user = info.context.user
        if user.is_anonymous or user.pk != self.pk:
            return None
        return self.email[0] + '*' * (self.email.index('@') - 1) + self.email[self.email.index('@'):]

class UserObject(UserType):
    class Meta:
        super(UserType)
        model = User
        interfaces = (relay.Node, )
        filter_fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'key': ['exact'],
        }
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
        input = UserInput()

    user = Field(UserType)

    def mutate(self, info, input = None):
        if info.context.user.is_anonymous:
            raise Exception('Not logged in')
        user = info.context.user
        user.username = input.username if input.username else user.username
        user.first_name = input.first_name if input.first_name else user.first_name
        user.last_name = input.last_name if input.last_name else user.last_name
        user.sex = input.sex if input.sex else user.sex
        user.dob = input.dob if input.dob else user.dob
        if input.image:
            user.image = ImageHandler(input.image).auto_image()
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
    register = CreateUser.Field()
    login = LoginUser.Field()
    update_me = UpdateUser.Field()

class Query(ObjectType):
    Users = DjangoFilterConnectionField(UserObject)
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

