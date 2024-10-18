import json
from datetime import datetime
import pytz

# Função que compara a hora atual com dias da semana e verifica se está dentro do horário comercial
# Se estiver dentro devolve Dentro, c.c. Fora
def compara_hora(request):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    sem_europa = datetime.now().weekday()
    timezone = pytz.timezone('America/Sao_Paulo')
    dt_america = (datetime.now(timezone)).strftime("%d/%m/%Y %H:%M:%S")
    sem_america = datetime.now(timezone).weekday()
    text = dt_america + ' , ' + dt_string + ' , ' + str(sem_america) + ' , ' + str(sem_europa)

    day_of_week = datetime.now(timezone).weekday()
    if(day_of_week >= 0 and day_of_week <= 4):
        if(datetime.now(timezone).hour < 8 or datetime.now(timezone).hour >= 17):
            text = 'Fora'
        else:
            text = 'Dentro'
    else:
        text = 'Fora'
        
    # Envia o json com a variável para o DF
    res = {
        "fulfillment_response": {
        "messages": [{"text": {"text": []}}]},
        'sessionInfo': {"parameters": {"validacao_hora": text}}
    }

    # Returns json
    return res
