import logging
import json
from xmlrpc.client import DateTime
import azure.functions as func
import os
import uuid

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials


#
# entrypoint for the azure function - called when the input trigger is fired. In this case, a new blob
# arriving in the image container. See function.json for information about the function bindings
#
def main(inBlob: func.InputStream,      # the input blob supplied by the trigger 
            outTable: func.Out[str],    # storage table to post results
            outBlob: func.Out[str]      # output blob to store results
            ):

    # log the trigger execution 
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {inBlob.name}\n"
                 f"Blob Size: {inBlob.length} bytes")


    # get the prediction service endpoing and key from the settings. These settings are set in local.settings.json. 
    # local.settings.json contains secret values we do not post to github. Use local.settings-sample.json as a template for your settings file
    # these settigns are uploaded to the function configuration when the function is created and you can upload new settings 
    # using the function extention in VS Code
    prediction_endpoint =  os.environ['prediction_endpoint'] 
    prediction_key = os.environ['prediction_key'] 

    vision_project_id = os.environ["vision_project_id"]
    vision_iteration_name = os.environ["vision_model_name"]


    logging.info(f"Endpoint: {prediction_endpoint}\n"
                f"project_id: {vision_project_id}\n"
                f"iteration_name: {vision_iteration_name}"
                )

    # configure the predictor with endpoint and authentication info
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

    # call the prediction service with the iamge data
    # here we are passing the image bytes to the API call but you could also specify a public URL to the blob 
    results = predictor.classify_image(
        vision_project_id, vision_iteration_name, inBlob.read())

    # write the predictions to a dictionary and encode to a json string
    predictions_dict = {}
    predictions_dict["file_name"]=inBlob.name
    for p in results.predictions:
        predictions_dict[p.tag_name] = p.probability

    predictions_str = json.dumps(predictions_dict)

    # log the prediction, post to the results queue and persist the predictions as a blob in the storage account
    logging.info(predictions_str)
    outBlob.set(predictions_str)

    rowKey = str(uuid.uuid4())

    data = {
        "rowKey" : rowKey
        , "partitionKey" : "result"
        , "result" : predictions_dict
    }


    logging.info(json.dumps(data))
    outTable.set(json.dumps(data))
 
