from django.utils import timezone
from django.test import TestCase

from cards.models import Answer, Card, Question
from decks.models import Deck

import json
from ast import literal_eval
import base64
from graphene_django.utils.testing import GraphQLTestCase
# Create your tests here.


def create_question(question_text):
    return Question.objects.create(question_text=question_text)


def get_question(id):
    return Question.objects.get(pk=id)


def create_answer(answer_text, question=None):
    return Answer.objects.create(answer_text=answer_text, question=question)


def get_answer(id):
    return Answer.objects.get(pk=id)


def create_card(question_text, answer_text, deck):
    return Card.objects.create(question_text=question_text, answer_text=answer_text, deck=deck)


def get_card(id):
    return Card.objects.get(pk=id)


def create_deck(name):
    return Deck.objects.create(name=name)


def get_deck(id):
    return Deck.objects.get(pk=id)
# test CRUD for question, answer and card


class QuestionModelTest(TestCase):

    def test_was_question_created_successfully(self):
        question = create_question("What is urine?")
        self.assertIsNotNone(question)

    def test_was_question_read_successfully(self):
        quest_txt = "What is urine?"
        question = create_question(quest_txt)
        self.assertEqual(get_question(question.id).question_text, quest_txt)

    def test_was_question_updated_successfully(self):
        quest_txt1 = "What is urine?"
        quest_txt2 = "What is the nervous system?"
        question = create_question(quest_txt1)
        question.question_text = quest_txt2
        question.save()
        self.assertEqual(get_question(question.id).question_text, quest_txt2)

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
        self.assertEqual(get_answer(answer.id).answer_text, answer_txt)

    def test_was_answer_updated_successfully(self):
        ans_txt1 = "filtered blood"
        ans_txt2 = "yellow liquid"
        answer = create_answer(ans_txt1)
        answer.answer_text = ans_txt2
        answer.save()
        self.assertEqual(get_answer(answer.id).answer_text, ans_txt2)

    def test_was_answer_deleted_successfully(self):
        ans_txt1 = "filtered blood"
        answer = create_answer(ans_txt1)
        res = answer.delete()
        self.assertEqual(res[0], 1)


class CardModelTest(TestCase):

    def test_was_card_created_successfully(self):
        deck = create_deck("myDeck")
        card = create_card(deck=deck, question_text="what is a prime number?",
                           answer_text="a number only divisible by itself and one.")
        self.assertIsNotNone(card)

    def test_was_card_read_successfully(self):
        deck = create_deck("myDeck")
        card = create_card(deck=deck, question_text="what is a prime number?",
                           answer_text="a number only divisible by itself and one.")
        self.assertIsNotNone(get_card(card.id))

    def test_was_card_updated_successfully(self):
        deck = create_deck("myDeck")
        card = create_card(deck=deck, question_text="what is a prime number?",
                           answer_text="a number only divisible by itself and one.")
        new_answer = "7 continents on the earth"
        card.answer_text = new_answer
        card.save()
        self.assertEqual(get_card(card.id).answer_text, new_answer)

    def test_was_card_deleted_successfully(self):
        deck = create_deck("myDeck")
        card = create_card(deck=deck, question_text="what is a prime number?",
                           answer_text="a number only divisible by itself and one.")
        res = card.delete()
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
            query getQuestion($id: ID!){
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

    def test_create_question(self):
        response = self.query(
            '''
            mutation createQuestion($input: QuestionInput!){
                createQuestion(questionInput: $input) {
                    question{
                        id
                        questionText
                    }
                }
            }
            ''',
            op_name='createQuestion',
            input_data={
                'questionText': 'What is the nervous system?'}
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        decoded = base64.b64decode(
            content["data"]["createQuestion"]["question"]["id"])
        num = decoded.split(b':')[1]
        question = get_question(num)
        self.assertEqual(question.id, int(num))
        self.assertEqual(question.question_text,
                         content["data"]["createQuestion"]["question"]["questionText"])

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

    def test_delete_question(self):
        question = create_question("What is urine?")
        response = self.query(
            '''
            mutation deleteQuestion($id: ID!) {
                deleteQuestion(id: $id) {
                    res
                }
            }
            ''',
            op_name='deleteQuestion',
            variables={'id': question.id}
        )

        content = json.loads(response.content)
        tup = literal_eval(content['data']['deleteQuestion']['res'])
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(1, int(tup[0]))
        with self.assertRaises(Question.DoesNotExist):
            get_question(question.id)
