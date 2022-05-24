import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from graphql import GraphQLError
from cards.models import Answer, Card, Question


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        only_fields = ("id", "question_text", "created_date")
        interfaces = (relay.Node,)


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        only_fields = ("id", "question", "answer_text", "created_date")
        interfaces = (relay.Node,)


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        only_fields = ("id", "question", "answer", "created_date")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    card = graphene.Field(CardType, id=graphene.String())
    question = graphene.Field(QuestionType, id=graphene.String())
    answer = graphene.Field(AnswerType, id=graphene.String())

    def resolve_card(root, info, id):
        # Querying a single question
        return Card.objects.get(pk=id)

    def resolve_question(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    def resolve_answer(root, info, id):
        # Querying a single question
        return Answer.objects.get(pk=id)

    all_cards = graphene.List(CardType)
    all_questions = graphene.List(QuestionType)
    all_answers = graphene.List(AnswerType)

    def resolve_all_cards(root, info, **kwargs):
        # Querying a list
        return Card.objects.all()

    def resolve_all_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_all_answers(root, info, **kwargs):
        # Querying a list
        return Answer.objects.all()
