from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import DetectRequest, TimeSeriesPoint, TimeGranularity, AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential
import azure.functions as func
import json
import logging
import os
import uuid
from datetime import datetime

###
### function entry point. triggered via http request from stream analytics job
### outputs results of anomaly detection to table storage
### 
def main(req: func.HttpRequest,
            outputmessage: func.Out[str]):
    
    logging.info('Python HTTP trigger function processed a request.')

    #
    # retrieve configuration variables 
    #
    ANOMALY_DETECTOR_SUBSCRIPTION_KEY = os.environ["anomaly_detector_subscription_key"]
    ANOMALY_DETECTOR_ENDPOINT = os.environ["anomaly_detector_endpoint"]

    # the body of the request should contain a json array with a timeseries of temperature readings
    req_body = req.get_json()
    logging.info(req_body)

    if (len(req_body) == 0):
        logging.info("empty body")
        return 

    # stream analytics outputs an array of windows. in our case we are only outputting one window
    temperature_readings = req_body[0]     

    # log the number of temperature readings in our time window
    logging.info(f"number of readings: {len(temperature_readings['details'])}")

    # convert the array of temperature readings into an array of TimeSeriesPoint objects 
    # expected by the anomaly detection service
    series = []
    for reading in temperature_readings["details"]:
        # convert the timeformat that we see in the event stream into the ISO expected by the anomaly detection service
        time_parts = f'{reading["time_utc"]}'.split(":")
        event_time= f'{reading["date_utc"]}T{time_parts[0]}:{time_parts[1]}:00Z'
        series.append(TimeSeriesPoint(
                        timestamp=datetime.fromisoformat(event_time), 
                        value=reading['temp_f']))


    # create a request object to send to the service
    request = DetectRequest(series=series, granularity=TimeGranularity.PER_MINUTE)

    # instantiate a client to the service
    client = AnomalyDetectorClient(AzureKeyCredential(ANOMALY_DETECTOR_SUBSCRIPTION_KEY), ANOMALY_DETECTOR_ENDPOINT)

    # send the request to the service
    response = client.detect_last_point(request)

    # format the output message
    rowKey = str(uuid.uuid4())
    data = {
        "PartitionKey": "result",
        "RowKey": rowKey,
        "is_anomaly": response.is_anomaly,
        "data": temperature_readings 
    }

    # stuff the output into the outputmessage object that is bound to our storage table 
    outputmessage.set(json.dumps(data))

    # log whether an anomaly was detected or not
    if response.is_anomaly:
        logging.info('The latest point is detected as anomaly.')
    else:
        logging.info('The latest point is not detected as anomaly.')



