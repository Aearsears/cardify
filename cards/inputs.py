
import graphene


class QuestionInput(graphene.InputObjectType):
    question_text = graphene.String(required=True)


class AnswerInput(graphene.InputObjectType):
    answer_text = graphene.String(required=True)
    question_id = graphene.Int(required=False)


class CardInput(graphene.InputObjectType):
    question_id = graphene.String(required=True)
    answer_id = graphene.Int(required=True)
    deck_id = graphene.Int(required=True)
