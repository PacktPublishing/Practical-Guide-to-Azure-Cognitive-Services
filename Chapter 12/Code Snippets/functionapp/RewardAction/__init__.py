import logging
from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import RewardRequest
from msrest.authentication import CognitiveServicesCredentials

import os

import azure.functions as func

from data.platters import get_platters
from data.users import get_context


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    event_id = req.params.get('event_id', '')
    reward = float(req.params.get('reward', '-1'))
    
    if event_id == '' or reward == -1:
        return func.HttpResponse("Please supply params event_id and reward", status_code=400)
    
    
    key = os.getenv("PERSONALIZER_KEY", "")
    endpoint = os.getenv("PERSONALIZER_ENDPOINT", "")

    client = PersonalizerClient(endpoint, CognitiveServicesCredentials(key))
    
    client.events.reward(event_id=event_id, value = reward)
    
    return func.HttpResponse("Reward {0} was applied to event id {1}".format(reward, event_id), status_code=200)
    
