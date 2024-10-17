import os
import json
import requests
import logging

def envia_pdf(request):
    request_json = request.get_json()
    numero_from = request_json['sessionInfo']['parameters']['author']
    url_media = request_json['sessionInfo']['parameters']['url_media'] # link bucket
    tipo_autent = request_json['sessionInfo']['parameters']['tipo_autent'] # 'application/pdf'
    num_bot = request_json['sessionInfo']['parameters']['ident_bot'] 
    logging.warning("numero usuario: " + numero_from + ", media: " + url_media + ", tipo_autent: " + tipo_autent + ", numero bot: " + num_bot)
        
    url = "https://api.twilio.com/2010-04-01/Accounts/{{ACCOUNT_SID}}/Messages.json"
    payload='From=whatsapp%3A%2B'+ str(num_bot) + '&Body=&To=' + str(numero_from).replace(":+","%3A%2B") + '&MediaUrl=' + str(url_media)
    logging.warning("payload" + payload)

    headers = {
        'Accept': tipo_autent,
        'Authorization': 'Basic ' + os.environ.get('Autenticacao'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    r = json.loads(response.content)
    logging.warning("resp. api" + str(r))

    # Envia no formato json para o DF
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                        ]
                    }
                }
            ]
        }
    }

    # Returns json
    return res