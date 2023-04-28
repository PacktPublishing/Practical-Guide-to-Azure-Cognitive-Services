import logging
from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import RankableAction, RewardRequest, RankRequest, RankResponse
from msrest.authentication import CognitiveServicesCredentials

import json, os, random

import azure.functions as func

from data.platters import actions_and_features
from data.users import user_profiles

def get_platters():
    res = []
    for platter_id, feat in actions_and_features.items():
        action = RankableAction(id=platter_id, features=[feat])
        res.append(action)
    return res


def get_context(user):
    location_context = {'location': random.choice(['west', 'east', 'midwest'])}
    season = {'season': random.choice(['spring', 'summer', 'fall', 'winter'])}
    cuisine_searched = {'cuisine_searched': random.choice(['italian', 'mexican', 'asian', 'american'])}
    res = [user_profiles.get(user, ''), location_context, season, cuisine_searched]
    return res


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user = req.params.get('user', '')
    if (user == ''):
        return func.HttpResponse("Please pass a name on the query string", status_code=400)

    user_context = get_context(user) 
    if (user_context[0] == ''):
        return func.HttpResponse("User not found", status_code=404)


    articles = get_platters()

    key = os.getenv("PERSONALIZER_KEY", "")
    endpoint = os.getenv("PERSONALIZER_ENDPOINT", "")

    client = PersonalizerClient(endpoint, CognitiveServicesCredentials(key))

    rank_request = RankRequest(actions=articles, context_features=user_context)
    
    rank_response = client.rank(rank_request=rank_request)

    recipe_list = {'user':user, 'event_id':rank_response.event_id, 'best_action': rank_response.reward_action_id , 'rankings':[]} # pyright: ignore[reportOptionalMemberAccess, reportGeneralTypeIssues]

    for ranking in enumerate(rank_response.ranking): # pyright: ignore[reportOptionalMemberAccess, reportGeneralTypeIssues]
        recipe_list['rankings'].append({'rank' : ranking[0],'id' : ranking[1].id, 'probability' : ranking[1].probability})
           
    return func.HttpResponse(json.dumps(recipe_list), mimetype="application/json")


