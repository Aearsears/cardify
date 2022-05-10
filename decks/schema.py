import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from graphene_django_crud.types import DjangoCRUDObjectType, resolver_hints
from decks.models import Deck


class DeckType(DjangoCRUDObjectType):

    class Meta:
        model = Deck
        exclude_fields = ()
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        return Deck.objects.all()
        # if info.context.user.is_authenticated:
        #     return Deck.objects.all()
        # else:
        #     return Deck.objects.none()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Not authorized, you must be logged in.')

        if "password" in data.keys():
            instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)


class Query(graphene.ObjectType):
    deck = DeckType.ReadField()

    all_decks = DeckType.BatchReadField()


class Mutation(graphene.ObjectType):

    deck_create = DeckType.CreateField()
    deck_update = DeckType.UpdateField()
    deck_delete = DeckType.DeleteField()
