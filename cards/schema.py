import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from graphene_django_crud.types import DjangoCRUDObjectType, resolver_hints

from cards.models import Answer, Card, Question


class QuestionType(DjangoCRUDObjectType):
    class Meta:
        model = Question
        only_fields = ("id", "question_text", "created_date")
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        return Question.objects.all()
        # if info.context.user.is_authenticated:
        #     return Question.objects.all()
        # else:
        #     return Question.objects.none()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        # if not info.context.user.is_authenticated:
        #     raise GraphQLError('Not authorized, you must be logged in.')

        # if "password" in data.keys():
        #     instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)


class AnswerType(DjangoCRUDObjectType):
    class Meta:
        model = Answer
        only_fields = ("id", "question", "answer_text", "created_date")
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        return Answer.objects.all()
        # if info.context.user.is_authenticated:
        #     return Answer.objects.all()
        # else:
        #     return Answer.objects.none()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Not authorized, you must be logged in.')

        if "password" in data.keys():
            instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)


class CardType(DjangoCRUDObjectType):
    class Meta:
        model = Card
        only_fields = ("id", "question", "answer", "created_date")
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        return Card.objects.all()
        # if info.context.user.is_authenticated:
        #     return Card.objects.all()
        # else:
        #     return Card.objects.none()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Not authorized, you must be logged in.')

        if "password" in data.keys():
            instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)


class Query(graphene.ObjectType):
    card = CardType.ReadField()
    question = QuestionType.ReadField()
    answer = AnswerType.ReadField()

    all_cards = CardType.BatchReadField()
    all_questions = QuestionType.BatchReadField()
    all_answers = AnswerType.BatchReadField()


class Mutation(graphene.ObjectType):

    question_create = QuestionType.CreateField()
    question_update = QuestionType.UpdateField()
    question_delete = QuestionType.DeleteField()

    answer_create = AnswerType.CreateField()
    answer_update = AnswerType.UpdateField()
    answer_delete = AnswerType.DeleteField()

    card_create = CardType.CreateField()
    card_update = CardType.UpdateField()
    card_delete = CardType.DeleteField()
