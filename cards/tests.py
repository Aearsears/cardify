from django.utils import timezone
from django.test import TestCase

from cards.models import Answer, Card, Question
from decks.models import Deck

# Create your tests here.


def create_question(question_text):
    return Question.objects.create(question_text=question_text, created_date=timezone.now())


def create_answer(question, answer_text):
    return Answer.objects.create(question=question, answer_text=answer_text, created_date=timezone.now())


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
        question = Question.objects.get(pk=question.id)
        question.question_text = quest_txt2
        question.save()
        self.assertEqual(Question.objects.get(
            pk=question.id).question_text, quest_txt2)

    def test_was_question_deleted_successfully(self):
        quest_txt1 = "What is urine?"
        question = create_question(quest_txt1)
        res = question.delete()
        self.assertEqual(res[0], 1)
