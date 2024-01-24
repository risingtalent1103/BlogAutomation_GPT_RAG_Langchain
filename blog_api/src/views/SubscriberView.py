# /src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.SubscriberModel import SubscriberModel, SubscriberSchema
from bs4 import BeautifulSoup
subscriber_api = Blueprint('subscriber_api', __name__)
subscriber_schema = SubscriberSchema()



def get_subscribers():
    """
    Create Blogpost Function
    """
    subscribers = SubscriberModel.get_all_subscribers()
    data = subscriber_schema.dump(subscribers)
    return custom_response(data, 200)
def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )