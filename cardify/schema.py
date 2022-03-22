import graphene
from graphene import relay
from graphene_django_crud.types import DjangoCRUDObjectType, resolver_hints

from graphql import GraphQLError

from django.contrib.auth.models import User

import cards.schema
import decks.schema


class UserType(DjangoCRUDObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)
        input_exclude_fields = ("last_login", "date_joined")
        interfaces = (relay.Node,)

    full_name = graphene.String()

    @resolver_hints(only=["first_name", "last_name"])
    @staticmethod
    def resolve_full_name(parent, info, **kwargs):
        return parent.get_full_name()

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        if info.context.user.is_authenticated:
            return User.objects.all()
        else:
            return User.objects.none()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Not authorized, you must be logged in.')

        if "password" in data.keys():
            instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)


class Query(cards.schema.Query, decks.schema.Query, graphene.ObjectType):
    me = graphene.Field(UserType)
    user = UserType.ReadField()
    all_users = UserType.BatchReadField()
    # user = relay.Node.Field(UserType)
    # all_users = DjangoFilterConnectionField(UserType)
    hello = graphene.String()

    def resolve_hello(root, info):
        return "world"

    def resolve_me(parent, info, **kwargs):
        if not info.context.user.is_autheticated:
            return None
        else:
            return info.context.user


class Mutation(cards.schema.Mutation, decks.schema.Mutation, graphene.ObjectType):

    user_create = UserType.CreateField()
    user_update = UserType.UpdateField()
    user_delete = UserType.DeleteField()


schema = graphene.Schema(query=Query, mutation=Mutation)
