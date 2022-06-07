
import graphene


class QuestionInput(graphene.InputObjectType):
    question_id = graphene.Int(required=False)
    question_text = graphene.String(required=True)


class AnswerInput(graphene.InputObjectType):
    answer_id = graphene.Int(required=False)
    answer_text = graphene.String(required=True)
    question_id = graphene.Int(required=False)


class CardInput(graphene.InputObjectType):
    card_id = graphene.Int(required=False)
    question_id = graphene.Int(required=False)
    answer_id = graphene.Int(required=False)
    deck_id = graphene.Int(required=False)
