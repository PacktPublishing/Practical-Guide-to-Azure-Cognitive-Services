import logging

import azure.functions as func
import http.client
import json
import urllib.parse
import os
import uuid

def create_service_connection(service_region, speech_key):

    logging.info(f"create service connection: {service_region}, {speech_key}")

    service_connection = http.client.HTTPSConnection(f"{service_region}.api.cognitive.microsoft.com")

    return service_connection

def get_http_headers(speech_key):
    headers = {
        'Ocp-Apim-Subscription-Key': f'{speech_key}',
        'Content-Type': 'application/json'
        }

    return headers


def transcribe_file(file_name, service_region, speech_key):

    logging.info(f"transcribe_file. {file_name}, {service_region}")


    payload = json.dumps({
        "contentUrls": [
            f"https://ch13storage.blob.core.windows.net/{file_name}"
        ],
        "properties": {
            "diarizationEnabled": False,
            "wordLevelTimestampsEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale": "en-US",
        "displayName": "Transcription using default model for en-US"
        })

    
    logging.info(f"payload: {payload}")

    service_connection = create_service_connection(service_region, speech_key)
    service_connection.request("POST", "/speechtotext/v3.0/transcriptions", payload, get_http_headers(speech_key))

    response_string = service_connection.getresponse().read().decode("utf-8")
    logging.info(f"response: {response_string}")
    dataDict = json.loads(response_string)


    transcription_id = dataDict['self'].split('/').pop()

    logging.info(f"transcription_id: {transcription_id}")

    return transcription_id


# def wait_for_transcription(transcription_id, service_region, speech_key):
#     service_connection = create_service_connection(service_region, speech_key)

#     payload = json.dumps('')

#     still_running = True
#     while still_running:

#         logging.log("waiting..")
#         time.sleep(5)
#         logging.log("checking..")

#         service_connection.request("GET", f"/speechtotext/v3.0/transcriptions/{transcription_id}", payload, get_http_headers(speech_key))
#         logging.log("checked..")

#         dataDict = json.loads(service_connection.getresponse().read().decode("utf-8"))

#         if dataDict["status"] != "Running":
#             still_running = False

#     return dataDict["status"]


# def get_transcription_file(transcription_id, service_region, speech_key) :
#     service_connection = create_service_connection(service_region, speech_key)
#     payload = json.dumps('')


#     service_connection.request("GET", f"/speechtotext/v3.0/transcriptions/{transcription_id}/files", payload, get_http_headers(speech_key))
#     dataDict = json.loads(service_connection.getresponse().read().decode("utf-8"))

#     for transcriptionFile in dataDict['values']:
#         if  transcriptionFile["kind"] == "Transcription":
#             file_url = transcriptionFile['links']["contentUrl"]
            
#             url_parts = urllib.parse.urlparse(file_url)
#             file_connection = http.client.HTTPSConnection(url_parts.hostname)
#             file_connection.request("GET", f"{url_parts.path}?{url_parts.query}")
#             file_content = file_connection.getresponse().read()
 
#             # set the output to the file_content
#     return file_content

# def delete_transcription(transcription_id, service_region, speech_key) :
#     service_connection = create_service_connection(service_region, speech_key)
#     payload = json.dumps('')
#     service_connection.request("DELETE", f"/speechtotext/v3.0/transcriptions/{transcription_id}", payload, get_http_headers(spee))



def main(newRecording: func.InputStream, outTable: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {newRecording.name}\n"
                 f"Blob Size: {newRecording.length} bytes")


    speech_key = os.environ["speech_key"]
    service_region = os.environ["service_region"]

    transcription_id = transcribe_file(newRecording.name, service_region, speech_key)

    rowKey = str(uuid.uuid4())

    data = {
        "rowKey" : str(uuid.uuid4())
        , "partitionKey" : "result"
        , "fileName" : newRecording.name
        , "transcriptionId" : transcription_id
        , "status" : "new" 
        , "statusCheckCount" : "0"
    }


    logging.info(json.dumps(data))
    outTable.set(json.dumps(data))


    # status = wait_for_transcription(transcription_id, service_region, speech_key)

    # if (status) == "Succeeded":
    #     payload = json.dumps('')

    #     file_content = get_transcription_file(transcription_id, service_region, speech_key)
    #     transcription.set(file_content)
    #     delete_transcription(transcription_id, service_region, speech_key)


