import json
import logging
import requests
import os

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    date_limit = req.params.get('date_limit')
    logging.debug(f"limit date provided : {date_limit}")
    

    api_url = os.getenv("URL_CRUD_AIGUILLON_DB") + f"/eqpugp?$filter=rodtdermod ge {date_limit}T00:00:00Z"
    logging.debug(f"api_url : {api_url}")

    try:
        response = requests.get(api_url,
                                headers={"Ocp-Apim-Subscription-Key": os.getenv("CRUD_APIM_SUBSCRIPTION_KEY")})
        logging.info('Successfull call :')
        logging.debug(response.json())
    
        return func.HttpResponse(body=json.dumps(response.json()["value"]),
                                 headers={"Content-Type" : "application/json"},
                                 status_code=200)
    except ValueError:
        logging.error(f"erreur lors de l'appel : {ValueError.with_traceback}")
        return func.HttpResponse(
             ValueError,
             status_code=500
        )
