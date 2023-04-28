from azure.data.tables import TableClient
import azure.functions as func
import datetime
import json
import logging
import os
import random

##
## entry point to the azure function - this function is trigered on a timer that fires 1/minute
## the purpose of this function is to simulate an event stream of temperature readings from a 
## refridgeration unit
##
## every time the function is triggered we will post a message on an event hub
## in a real world scenario you would not have a refridgeration unit publishing directly 
## to Azure - you would probably have an edge gateway device in the middle, and you might be 
## using IoT specific services such as IoT Central; however, for the purposes of this example
## the logic within Azure to pick up those message is very much the same. 
## 
## this fridge is set to 43.2 degrees F. under normal conditions the temperature reading will be 
## within a degree of the set temp. 
## 
## to simulate an anomaly, we will read from an azure storage table. If there is an entry in the table
## we will use that value instead of the set temp. 
##
## Parameters: 
##      mytimer -- the timer that triggered te function
##      tempoverride -- an entity from the tempoverride azure storage table if one exists
##  Return:
##      the return of the function is bound to an event hub that will receive the message and store
##      the message until it is consumed (in our example by an Azure Stream Analytics job)
##
def main(mytimer: func.TimerRequest,
            tempoverride
        ) -> str:


    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # retieve configuration information
    STORAGE_CONNECTION_STRING = os.environ["AzureWebJobsStorage"]

    # log any temp overrides that are set
    logging.info(f'temp overrides: {tempoverride}')

    # get the current date and time and convert to a streing formatted in a way that you might 
    # see in a refridgeration unit's telemetry stream
    now = datetime.datetime.utcnow()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')

    # init the temp variable that we will use to format the output message 
    temperature = 0.0

    # convert the tempoverride entity to a json object
    tempoverride_json = json.loads(tempoverride)

    # if there is an entity in the tempoverride table
    if len(tempoverride_json)>0:
        # set temp to the value found in the table enttiy 
        temperature = float(tempoverride_json[0]["set_temp"])
        
        # delete the override from the table so it is not reused
        table_client = TableClient.from_connection_string(STORAGE_CONNECTION_STRING, "temperatureoverride")
        table_client.delete_entity("temps", tempoverride_json[0]["RowKey"])
    else:
        # if there is no override set, set the temperature to a randum number near 43.2 degrees
        # use a normal distrition and a pretty tight standard deviation that allows for some 
        # variability but will usually vall within 1 degreee of the set temperature  
        temperature = round(random.normalvariate(43.2, .3), 1)

    # format the output message
    message = {
                'date_utc': f'{date_string}',
                'time_utc': f'{time_string}',
                'model': 'DWE',
                'chiller_serial': '16346834',
                'pod_serial': '19072218',
                'temp_f': temperature
              }


    # log the function execution and the output message
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    logging.info(f'message: {message}')

    # return the message - the return value is bound to an event hub
    return json.dumps(message)
