import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from cards.models import Answer, Card, Question

from django.contrib.auth.models import User


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "question_text", "created_date")
        filter_fields = {'id': ['exact'], 'question_text': ['icontains']}
        interfaces = (relay.Node,)


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("id", "question", "answer_text", "created_date")
        filter_fields = {'id': ['exact'], 'answer_text': ['icontains']}
        interfaces = (relay.Node,)


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        fields = ("id", "question", "answer", "created_date")
        filter_fields = {'id': ['exact']}
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    card = relay.Node.Field(CardType)
    question = relay.Node.Field(QuestionType)
    answer = relay.Node.Field(AnswerType)

    all_cards = DjangoFilterConnectionField(CardType)
    all_questions = DjangoFilterConnectionField(QuestionType)
    all_answers = DjangoFilterConnectionField(AnswerType)

    # all_cards_test = graphene.List(CardType)

    # def resolve_all_cards_test(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return Card.objects.all()
