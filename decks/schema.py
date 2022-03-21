import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from decks.models import Deck


class DeckType(DjangoObjectType):
    class Meta:
        model = Deck
        fields = ("id", "name", "created_date")
        filter_fields = {'id': ['exact']}
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    deck = relay.Node.Field(DeckType)

    all_decks = DjangoFilterConnectionField(DeckType)
