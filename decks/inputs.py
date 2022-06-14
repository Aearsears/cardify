
import graphene


class DeckInput(graphene.InputObjectType):
    deck_id = graphene.ID(required=False)
    deck_name = graphene.String(required=True)
