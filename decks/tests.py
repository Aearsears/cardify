from django.test import TestCase
from cards.models import Answer, Card, Question

from decks.models import Deck

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
        print(res)
        # deletes deck and cards in the deck
        self.assertEqual(res[0], 2)
