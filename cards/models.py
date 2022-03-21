from tkinter import CASCADE
from django.db import models

from decks.models import Deck

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.answer_text

# TODO: need to clearly define the cascade property to ensure it reflects what I want it to do


class Card(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)
