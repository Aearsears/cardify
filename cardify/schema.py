import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from graphql import GraphQLError

from django.contrib.auth.models import User

import cards.schema
import decks.schema


class UserType(graphene.ObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)
        input_exclude_fields = ("last_login", "date_joined")
        interfaces = (relay.Node,)


class Query(cards.schema.Query, decks.schema.Query, graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.String())
    all_users = graphene.List(UserType)
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

    def resolve_all_users(root, info, **kwargs):
        # Querying a list
        return User.objects.all()

    def resolve_user(root, info, id):
        # Querying a single question
        return User.objects.get(pk=id)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        username = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, id, username):
        user = User.objects.get(pk=id)
        user.username = username
        user.save()
        # Notice we return an instance of this mutation
        return UpdateUserMutation(username=user)


class Mutation(decks.schema.Mutation, cards.schema.Mutation, graphene.ObjectType):
    update_user = UpdateUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
