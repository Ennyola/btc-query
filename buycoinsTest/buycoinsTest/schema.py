import graphene
from getprice.schema import Query as priceQuery

class Query(priceQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)