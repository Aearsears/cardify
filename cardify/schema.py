import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User

import cards.schema
import decks.schema


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password",
                  "groups", "user_permissions", "is_staff", "last_login", "date_joined")
        filter_fields = {'id': ['exact'],
                         'username': ['exact'], 'email': ['exact']}
        interfaces = (relay.Node,)


class Query(cards.schema.Query, decks.schema.Query, graphene.ObjectType):
    user = relay.Node.Field(UserType)
    all_users = DjangoFilterConnectionField(UserType)


schema = graphene.Schema(query=Query)
