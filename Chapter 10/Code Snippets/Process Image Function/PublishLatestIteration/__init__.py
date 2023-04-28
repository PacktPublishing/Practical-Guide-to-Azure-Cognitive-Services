from cmath import log
import logging
import os
import datetime
import azure.functions as func
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# entry point to the function 
# this function runs on a timer. the schedule for the timer is located in the function.json file. 
# when the function executes it will get the list of iterations defined in the training endpoint, find the latest created 
# iteration and publish it to the prediction resource for use in future predictions

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # retrieve endpoint and project ids from environment files (as specified in localsettings.json)
    training_endpoint = os.getenv("training_endpoint")
    training_key = os.getenv("training_key")

    project_id = os.getenv("vision_project_id")
    model_name = os.getenv("vision_model_name")

    prediction_resource = os.getenv("prediction_resource")

    # set up API key to communicate with the CustomVision trainer and create the training client
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    trainer = CustomVisionTrainingClient(training_endpoint, credentials)

    # connect to the vision project and retrieve a list of training iterations
    project = trainer.get_project(project_id)
    iterations = trainer.get_iterations(project_id)

    # find the latest created iteration
    latest_iteration = iterations[0]
    for iteration in iterations:
        if iteration.created > latest_iteration.created:
            latest_iteration = iteration

    # if the latest iteration has completed training and it is not already published it, publish the model to the prediction resource
    # we will use the model name "CurrentModel" as defined in localsettings so that the ProcessNewImage api has a consistent model name to use
    # as we publish new iterations
    # note that the prediction resource is an azure resource ID to the prediction resource defined in the resource group. 
    # we need to explicitly state overwrite=True in the function call to overwrite the model 
    if latest_iteration.status == "Completed" and latest_iteration.publish_name != model_name:
        trainer.publish_iteration(project.id, latest_iteration.id, model_name, prediction_resource, overwrite=True)
        logging.info("iteration {latest_iteration.name} published")
    else:
        logging.info("there was no new iteration to publish")



