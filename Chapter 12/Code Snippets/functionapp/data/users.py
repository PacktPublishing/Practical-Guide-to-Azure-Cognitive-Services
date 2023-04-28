from azure.cognitiveservices.personalizer.models import RankableAction, RewardRequest, RankRequest
import datetime, json, os, time, uuid, random

user_profiles = {
    'Andy': {
        'company_size': 'large', 
        'avg_order_size': '0-20',
        'orders_per_month': '10-20',
        'allergies': 'none'
    },
    'Tim': {
        'company_size': 'large', 
        'avg_order_size': '20-50',
        'orders_per_month': '20-50',
        'allergies': 'shellfish'
    },
    'Paul': {
        'company_size': 'small', 
        'avg_order_size': '20-50',
        'orders_per_month': '20-50',
        'allergies': 'none'
    },
    'Scott': {
        'company_size': 'large', 
        'avg_order_size': '50-100',
        'orders_per_month': '10-20',
        'allergies': 'none'
    },
    'Chris': {
        'company_size': 'small', 
        'avg_order_size': '0-20',
        'orders_per_month': '10-20',
        'allergies': 'shellfish'
    }
}

def get_context(user):
    location_context = {'location': random.choice(['west', 'east', 'midwest'])}
    season = {'season': random.choice(['spring', 'summer', 'fall', 'winter'])}
    cuisine_searched = {'cuisine_searched': random.choice(['italian', 'mexican', 'asian', 'american'])}
    res = [user_profiles.get(user, ''), location_context, season, cuisine_searched]
    return res

