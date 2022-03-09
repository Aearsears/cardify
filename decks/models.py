from django.db import models
# to avoid circular imports
# from django.apps import apps
# MyModel1 = apps.get_model('app1', 'MyModel1')

# Create your models here.


class Deck(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.name
