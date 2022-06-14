from ast import literal_eval
import base64
import json
from django.test import TestCase
from cards.models import Answer, Card, Question

from decks.models import Deck

from graphene_django.utils.testing import GraphQLTestCase
# Create your tests here.


def create_question(question_text):
    return Question.objects.create(question_text=question_text)


def get_question(id):
    return Question.objects.get(pk=id)


def create_answer(answer_text, question=None):
    return Answer.objects.create(answer_text=answer_text, question=question)


def create_card(question, answer, deck):
    return Card.objects.create(question=question, answer=answer, deck=deck)


def create_deck(name):
    return Deck.objects.create(name=name)


def get_deck(id):
    return Deck.objects.get(pk=id)

# test CRUD for card


class DeckModelTest(TestCase):

    def test_was_deck_created_successfully(self):
        deck = create_deck("My Study Deck")
        self.assertIsNotNone(deck)

    def test_was_deck_read_successfully(self):
        deckname = "GEO521"
        deck = create_deck(deckname)
        self.assertEqual(Deck.objects.get(
            pk=deck.id).name, deckname)

    def test_was_deckname_updated_successfully(self):
        deckname1 = "GEO521"
        deckname2 = "MATH330"
        deck = create_deck(deckname1)
        deck.name = deckname2
        deck.save()
        self.assertEqual(Deck.objects.get(
            pk=deck.id).name, deckname2)

    def test_was_deck_deleted_successfully(self):
        deckname = "POLI340"
        deck = create_deck(deckname)
        res = deck.delete()
        self.assertEqual(res[0], 1)

    def test_was_deck_and_card_deleted_successfully(self):
        deck = create_deck("my study deck")
        question = create_question("What is urine?")
        answer = create_answer("filtered blood", question=question)
        card = create_card(question=question, answer=answer, deck=deck)
        res = deck.delete()
        # deletes deck and cards in the deck
        self.assertEqual(res[0], 2)


class GraphQLTestCase(GraphQLTestCase):
    def test_get_deck_by_id(self):
        deck = create_deck("My Deck")
        response = self.query(
            '''
            query getDeck($id: ID!){
                deckById(id: $id) {
                    id
                }
            }
            ''',
            op_name='getDeck',
            variables={'id': deck.id}
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        decoded = base64.b64decode(
            content["data"]["deckById"]["id"])
        num = decoded.split(b':')[1]
        self.assertEqual(deck.id, int(num))

    def test_update_deck(self):
        deck = create_deck("my deck")
        response = self.query(
            '''
            mutation updateDeck($input:DeckInput!) {
                updateDeck(deckInput: $input) {
                    deck{
                        name
                    }
                }
            }
            ''',
            op_name='updateDeck',
            input_data={'deckId': deck.id,
                        'deckName': 'COMP250'}
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertNotEqual(deck.name,
                            content["data"]["updateDeck"]["deck"]["name"])

    def test_delete_deck(self):
        deck = create_deck("myDeck")
        response = self.query(
            '''
            mutation deleteDeck($id: ID!) {
                deleteDeck(id: $id) {
                    res
                }
            }
            ''',
            op_name='deleteDeck',
            variables={'id': deck.id}
        )

        content = json.loads(response.content)
        tup = literal_eval(content['data']['deleteDeck']['res'])
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(1, int(tup[0]))
        with self.assertRaises(Deck.DoesNotExist):
            get_deck(deck.id)
