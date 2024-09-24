import channels_graphql_ws
import graphene

class MySubscription(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Leave only latest 64 messages in the server queue.
    notification_queue_limit = 64

    # Subscription payload.
    event = graphene.String()

    class Arguments:
        """That is how subscription arguments are defined."""
        pass

    @staticmethod
    def subscribe(root, info):
        """Called when user subscribes."""
        # Return the list of subscription group names.
        return ["my_subscription"]

    @staticmethod
    def publish(payload, info):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `None` if you wish to
        # suppress the notification to a particular client. For example,
        # this allows to avoid notifications for the actions made by
        # this particular client.

        return MySubscription(event=f"Event triggered (by hello query): {str(payload)}")

class Subscription(graphene.ObjectType):
    test_subscription = MySubscription.Field()
