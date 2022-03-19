import graphene

import cards.schema


class Query(cards.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
