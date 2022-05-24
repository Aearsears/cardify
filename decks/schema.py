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
    questions = graphene.List(DeckType)
    question_by_id = graphene.Field(DeckType, id=graphene.String())

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Deck.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Deck.objects.get(pk=id)


class UpdateDeckMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    question = graphene.Field(DeckType)

    @classmethod
    def mutate(cls, root, info, name, id):
        deck = Deck.objects.get(pk=id)
        deck.name = name
        deck.save()
        # Notice we return an instance of this mutation
        return UpdateDeckMutation(deck=deck)


class Mutation(graphene.ObjectType):
    update_question = UpdateDeckMutation.Field()
