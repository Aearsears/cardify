import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from graphql import GraphQLError
from cards.models import Answer, Card, Question


class QuestionType(DjangoObjectType):
    class Meta:
        model = Card
        exclude_fields = ()
        interfaces = (relay.Node,)


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        exclude_fields = ()
        interfaces = (relay.Node,)


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        exclude_fields = ()
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
        return Card.objects.get(pk=id)

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
        return Card.objects.all()

    def resolve_all_answers(root, info, **kwargs):
        # Querying a list
        return Answer.objects.all()


class UpdateQuestionMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        # question_text = graphene.String(required=True)

    # The class attributes define the response of the mutation
    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, id, question_text):
        question = Question.objects.get(pk=id)
        question.question_text = question_text
        question.save()
        # Notice we return an instance of this mutation
        return UpdateQuestionMutation(question=question)


class UpdateAnswerMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        answer_text = graphene.String(required=True)
        # question = graphene.Argument(QuestionType)

    # The class attributes define the response of the mutation
    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, id, answer_text, question=None):
        answer = Answer.objects.get(pk=id)
        answer.answer_text = answer_text
        # if(question):
        # answer.question = question
        answer.save()
        # Notice we return an instance of this mutation
        return UpdateAnswerMutation(answer=answer)


class UpdateCardMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    card = graphene.Field(CardType)

    @classmethod
    def mutate(cls, root, info, id):
        card = Card.objects.get(pk=id)
        card.save()
        # Notice we return an instance of this mutation
        return UpdateCardMutation(card=card)


class CreateQuestionMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        question_text = graphene.String(required=True)

    # The class attributes define the response of the mutation
    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, question_text):
        question = Question(question_text=question_text)
        question.save()
        # Notice we return an instance of this mutation
        return CreateQuestionMutation(question=question)


class CreateAnswerMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        answer_text = graphene.String(required=True)

    # The class attributes define the response of the mutation
    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, answer_text):
        answer = Answer(answer_text=answer_text)
        answer.save()
        # Notice we return an instance of this mutation
        return CreateAnswerMutation(answer=answer)


class CreateCardMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        question_text = graphene.String(required=True)

    # The class attributes define the response of the mutation
    card = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, card):
        card = Card(name=card)
        card.save()
        # Notice we return an instance of this mutation
        return CreateCardMutation(question=card)


class DeleteQuestionMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    # (1, {'blog.Entry': 1})
    # the number of objects deleted and a dictionary with the number of deletions per object type
    res = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        question = Question.objects.get(pk=id)
        res = question.delete()
        # Notice we return an instance of this mutation
        return DeleteQuestionMutation(res=res)


class DeleteAnswerMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    # (1, {'blog.Entry': 1})
    # the number of objects deleted and a dictionary with the number of deletions per object type
    res = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        answer = Answer.objects.get(pk=id)
        res = answer.delete()
        # Notice we return an instance of this mutation
        return DeleteAnswerMutation(res=res)


class DeleteCardMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    # (1, {'blog.Entry': 1})
    # the number of objects deleted and a dictionary with the number of deletions per object type
    res = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        card = Card.objects.get(pk=id)
        res = card.delete()
        # Notice we return an instance of this mutation
        return DeleteCardMutation(res=res)


class Mutation(graphene.ObjectType):
    update_question = UpdateQuestionMutation.Field()
    create_question = CreateQuestionMutation.Field()
    delete_question = DeleteQuestionMutation.Field()

    update_answer = UpdateAnswerMutation.Field()
    create_answer = CreateAnswerMutation.Field()
    delete_answer = DeleteAnswerMutation.Field()

    update_card = UpdateCardMutation.Field()
    create_card = CreateCardMutation.Field()
    delete_card = DeleteCardMutation.Field()
