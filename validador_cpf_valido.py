import json

# funcao que recebe parâmetros de uma sessão do DialogFlow (dentre eles CPF)
# devolve true caso seja um CPF válido, False c.c.
def valida_cpf(request):
  request_json = request.get_json()
  if('.' in request_json['sessionInfo']['parameters']['cpf']):
    cpf = int(request_json['sessionInfo']['parameters']['cpf'].replace(".","").replace("-",""))
  else:
    cpf = int(request_json['sessionInfo']['parameters']['cpf'])
    
  digitos = cpf % 100
  iniciais = cpf / 100

  vet = []
  a = int(iniciais)

  while(len(vet) != 9):
    a = iniciais % 10
    vet.append(a)
    iniciais = iniciais / 10

  soma1 = 0
  cont = 9

  for i in vet:
    soma1 += (int(i)*cont)
    cont -= 1
  dv1 = soma1 % 11
  if(dv1 == 10):
    dv1 = 0

  soma2 = dv1 * 9
  cont = 8
  for i in vet:
    soma2 += (int(i) * cont)
    cont -= 1
  dv2 = soma2 % 11
  if(dv2 == 10):
    dv2 = 0

  dvs = dv1 * 10 + dv2
  if(dvs == digitos):
    result = True
  else:
    result = False


  # formato para devolver para o DialogFlow
  res = {
    "fulfillment_response": {
      "messages": [{"text": {"text": []}}]},
      'sessionInfo': {"parameters": {"validacao_cpf": result}}
  }

  # Returns json
  return res
