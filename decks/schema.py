import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from decks.models import Deck


class DeckType(DjangoObjectType):

    class Meta:
        model = Deck
        exclude_fields = ()
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    decks = graphene.List(DeckType)
    deck_by_id = graphene.Field(DeckType, id=graphene.Int())

    def resolve_decks(root, info, **kwargs):
        # Querying a list
        return Deck.objects.all()

    def resolve_deck_by_id(root, info, id):
        # Querying a single question
        return Deck.objects.get(pk=id)


class UpdateDeckMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deck = graphene.Field(DeckType)

    @classmethod
    def mutate(cls, root, info, name, id):
        deck = Deck.objects.get(pk=id)
        deck.name = name
        deck.save()
        # Notice we return an instance of this mutation
        return UpdateDeckMutation(deck=deck)


class CreateDeckMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    deck = graphene.Field(DeckType)

    @classmethod
    def mutate(cls, root, info, name):
        deck = Deck(name=name)
        deck.save()
        # Notice we return an instance of this mutation
        return CreateDeckMutation(deck=deck)


class DeleteDeckMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    # (1, {'blog.Entry': 1})
    # the number of objects deleted and a dictionary with the number of deletions per object type
    res = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        deck = Deck.objects.get(pk=id)
        res = deck.delete()
        # Notice we return an instance of this mutation
        return DeleteDeckMutation(res=res)


class Mutation(graphene.ObjectType):
    update_deck = UpdateDeckMutation.Field()
    create_deck = CreateDeckMutation.Field()
    delete_deck = DeleteDeckMutation.Field()
