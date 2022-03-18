from django.contrib import admin
from cards.models import Card

from decks.models import Deck

# Register your models here.


class CardInline(admin.TabularInline):
    model = Card


class DeckAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date Information', {'fields': ['created_date']})
    ]
    list_display = ('id', 'name', 'created_date')
    list_filter = ('name', 'created_date')
    search_fields = ['name']
    inlines = [CardInline]


admin.site.register(Deck, DeckAdmin)
