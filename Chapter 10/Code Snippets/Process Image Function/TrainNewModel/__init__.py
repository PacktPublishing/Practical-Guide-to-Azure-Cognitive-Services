import logging
import datetime
import os
from xmlrpc.client import DateTime

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

import azure.functions as func

# entry point to the function 
# this function runs on a timer. the schedule for the timer is located in the function.json file. 
# when the function executes it will kick off training for a new iteration in the custom vision project and include any new tagged images 
# as the training job may take longer than the 10 minute max duration for an azure function using our consumption plan
# we seperate the tasks of training a new iteration and publishing the iteration into seperate functions

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


    # retrieve endpoint and project ids from environment files (as specified in localsettings.json)
    training_endpoint = os.environ['training_endpoint']
    training_key = os.environ['prediction_key']

    project_id = os.environ['vision_project_id']

    # set up API key to communicate with the CustomVision trainer and create the training client
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    trainer = CustomVisionTrainingClient(training_endpoint, credentials)

    # find the latest created iteration
    iterations = trainer.get_iterations(project_id)
    latest_iteration = iterations[0]
    for iteration in iterations:
        if iteration.created > latest_iteration.created:
            latest_iteration = iteration

    workspace_image_count = trainer.get_image_count(project_id)
    iteation_image_count = trainer.get_image_count(project_id=project_id, iteration_id=latest_iteration.id)

    # if there have been new images added to the project since the latest iteration 
    # connect to the vision project and kickoff a training job
    if workspace_image_count > iteation_image_count:    
        project = trainer.get_project(project_id)
        iteration = trainer.train_project(project.id)

    logging.info('iteration training has begun.')
    