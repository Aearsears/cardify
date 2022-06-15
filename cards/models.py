from tkinter import CASCADE
from django.db import models

from decks.models import Deck

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, null=True)
    answer_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer_text

# TODO: need to clearly define the cascade property to ensure it reflects what I want it to do


class Card(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.SET_NULL, null=True)
    answer = models.OneToOneField(Answer, on_delete=models.SET_NULL, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, null=True)
    answer_text = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
