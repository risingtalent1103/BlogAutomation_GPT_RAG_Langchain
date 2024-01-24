# /src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.GoldPriceModel import GoldPriceModel, GoldPriceSchema
from bs4 import BeautifulSoup
goldprice_api = Blueprint('goldprice_api', __name__)
goldprice_schema = GoldPriceSchema()



@goldprice_api.route('/', methods=['GET'])
def get_current_gold_price():
    """
    Create Blogpost Function
    """
    price = GoldPriceModel.get_current_price()
    data = goldprice_schema.dump(price)
    return custom_response(data, 200)
def save_gold_price(data):
    """
    Create Blogpost Function
    """
    data = goldprice_schema.load(data)
    price = GoldPriceModel(data)
    price.save()
    

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

