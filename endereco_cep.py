import json
import requests
import logging

# Pega o endereço completo da pessoa a partir do CEP
def endereco(request):
    req = request.get_json()
    cep = req['sessionInfo']['parameters']['cep']
    url = "https://viacep.com.br/ws/" + str(cep)+ "/json/"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    logging.warning("response: " + str(response))
    r = json.loads(response.text)
    logging.warning("r: " + str(r))

    if('erro' in r):
        erro = "true"
        text = ""
        bairro = ""
        cidade = ""
        logradouro = ""
        estado = ""
        pergunta_novamente = "false"
    else:
        if('logradouro' in r and r['logradouro'] == "" and r['localidade'] != ""):
            erro = "false"
            text = ""
            bairro = ""
            cidade = ""
            logradouro = ""
            estado = ""
            pergunta_novamente = "true"
        else:
            text = "Seu endereço é: *" + str(r['logradouro']) + " - " + str(r['bairro']) + ", " + str(r['localidade']) + ", " + str(r['uf']) + " - " + cep + "*?"
            erro = "false"
            logradouro = r['logradouro']
            bairro = r['bairro']
            cidade = r['localidade']
            estado = r['uf']
            erro = "false"
            pergunta_novamente = "false"
    
    # Envia os parâmetros e o texto para o DF
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            text
                        ]
                    }
                }
            ]
        },
        'sessionInfo': {
            "parameters": {
                "bairro" : bairro,
                "cidade": cidade,
                "logradouro": logradouro,
                "estado": estado,
                "erro": erro,
                "pergunta_novamente": pergunta_novamente
            }
        }
    }

    # Returns json
    return res