import graphene
import requests
from graphene_django import DjangoObjectType
from .models import Price

class CalculatePriceType(graphene.ObjectType):
    code = graphene.String()
    symbol = graphene.String()
    price = graphene.Float()
    description = graphene.String()

class Query:
    calculatePrice = graphene.Field(CalculatePriceType, queryType = graphene.String(), margin = graphene.Float(), exchangeRate = graphene.Float())

    #since type is a keyword in python, queryType is passed as an arguement instead
    def resolve_calculatePrice(self, info, queryType, margin, exchangeRate):
        #get the price of bitcoin from coindesk api
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        response = response.json()
        value = response['bpi']['USD']['rate']
        apiValueRetrieved = float(value.replace(',',""))

        try:
            if queryType == "sell":
                #get the margin percent of the retrieved price then subtract from the recieved price
                valuePercentage = apiValueRetrieved * (margin/100)
                btcAmountInUSD = apiValueRetrieved - valuePercentage
                nairaValue = btcAmountInUSD * exchangeRate
            if queryType == "buy":
                #get the margin percent of the retrieved price then add from the recieved price
                valuePercentage = apiValueRetrieved * (margin/100)  
                btcAmountInUSD = apiValueRetrieved + valuePercentage
                nairaValue = btcAmountInUSD * exchangeRate
            if margin < 0 or exchangeRate < 0 :
                return None
         
            return CalculatePriceType( code = "NGN", symbol = "₦ naira", price = nairaValue, description = "Nigerian Naira" )
        except:
            return None
        
    