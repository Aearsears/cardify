from django.utils import timezone
from django.test import TestCase

from cards.models import Answer, Card, Question
from decks.models import Deck

import json
import base64
from graphene_django.utils.testing import GraphQLTestCase
# Create your tests here.


def create_question(question_text):
    return Question.objects.create(question_text=question_text)


def get_question(id):
    return Question.objects.get(pk=id)


def create_answer(answer_text, question=None):
    return Answer.objects.create(answer_text=answer_text, question=question)


def create_card(question, answer, deck):
    return Card.objects.create(question=question, answer=answer, deck=deck, created_date=timezone.now())


def create_deck(name):
    return Deck.objects.create(name=name, created_date=timezone.now())


# test CRUD for question, answer and card
class QuestionModelTest(TestCase):

    def test_was_question_created_successfully(self):
        question = create_question("What is urine?")
        self.assertIsNotNone(question)

    def test_was_question_read_successfully(self):
        quest_txt = "What is urine?"
        question = create_question(quest_txt)
        self.assertEqual(Question.objects.get(
            pk=question.id).question_text, quest_txt)

    def test_was_question_updated_successfully(self):
        quest_txt1 = "What is urine?"
        quest_txt2 = "What is the nervous system?"
        question = create_question(quest_txt1)
        question.question_text = quest_txt2
        question.save()
        self.assertEqual(Question.objects.get(
            pk=question.id).question_text, quest_txt2)

    def test_was_question_deleted_successfully(self):
        quest_txt1 = "What is urine?"
        question = create_question(quest_txt1)
        res = question.delete()
        self.assertEqual(res[0], 1)

    def test_was_question_and_answer_deleted_successfully(self):
        question = create_question("What is urine?")
        answer = create_answer("filtered blood", question=question)
        res = question.delete()
        # deletes one question and one answer
        self.assertEqual(res[0], 2)


class AnswerModelTest(TestCase):

    def test_was_answer_created_successfully(self):
        answer = create_answer("filtered blood")
        self.assertIsNotNone(answer)

    def test_was_answer_read_successfully(self):
        answer_txt = "filtered blood"
        answer = create_answer(answer_txt)
        self.assertEqual(Answer.objects.get(
            pk=answer.id).answer_text, answer_txt)

    def test_was_answer_updated_successfully(self):
        ans_txt1 = "filtered blood"
        ans_txt2 = "yellow liquid"
        answer = create_answer(ans_txt1)
        answer.answer_text = ans_txt2
        answer.save()
        self.assertEqual(Answer.objects.get(
            pk=answer.id).answer_text, ans_txt2)

    def test_was_answer_deleted_successfully(self):
        ans_txt1 = "filtered blood"
        answer = create_answer(ans_txt1)
        res = answer.delete()
        self.assertEqual(res[0], 1)


class GraphQLTestCase(GraphQLTestCase):
    def test_is_endpoint_live(self):
        response = self.query(
            '''
            query hello{
                hello
            }
            ''',
            op_name='hello'
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

    def test_get_question_by_id(self):
        question = create_question("What is urine?")
        response = self.query(
            '''
            query getQuestion($id: Int!){
                question(id: $id) {
                    id
                    questionText
                }
            }
            ''',
            op_name='getQuestion',
            variables={'id': question.id}
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        decoded = base64.b64decode(
            content["data"]["question"]["id"])
        num = decoded.split(b':')[1]
        self.assertEqual(question.id, int(num))
        self.assertEqual(question.question_text,
                         content["data"]["question"]["questionText"])

    def test_update_question(self):
        question = create_question("What is urine?")
        response = self.query(
            '''
            mutation changeQuestion($input: QuestionInput!) {
                updateQuestion(questionInput: $input) {
                    question{
                        questionText
                    }
                }
            }
            ''',
            op_name='changeQuestion',
            input_data={'questionId': question.id,
                        'questionText': 'What is the nervous system?'}
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertNotEqual(question.question_text,
                            content["data"]["updateQuestion"]["question"]["questionText"])
