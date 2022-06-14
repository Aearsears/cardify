
import graphene


class QuestionInput(graphene.InputObjectType):
    question_id = graphene.ID(required=False)
    question_text = graphene.String(required=True)


class AnswerInput(graphene.InputObjectType):
    answer_id = graphene.ID(required=False)
    answer_text = graphene.String(required=True)
    question_id = graphene.ID(required=False)


class CardInput(graphene.InputObjectType):
    card_id = graphene.ID(required=False)
    question_id = graphene.ID(required=False)
    answer_id = graphene.ID(required=False)
    deck_id = graphene.ID(required=False)
