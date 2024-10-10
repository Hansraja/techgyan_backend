import graphene


class CreatorNotificationEnum(graphene.Enum):
    '''Type of Notification'''
    ALL = 'all'
    PERSONALIZED = 'personalized'
    NONE = 'none'

class CreatorFollowedObject(graphene.ObjectType):
    by_me = graphene.Boolean()
    notif_pref = CreatorNotificationEnum()