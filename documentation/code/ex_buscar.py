import requests

def buscarMedicamento(name, wordList = [], ...):
	page = 1
	errorMax = 5

	melhorCandidato = {'candidato' : None, 'afinidade' : 0,
		'termos' : [], 'sobras':0}

	while len(name) > 1 and errorMax>0:

		url = f'https://consultas.anvisa.gov.br/api/consulta/bulario?count=100&filter%5BnomeProduto%5D={name}&page={page}'

		try:
			response = requests.get(url, headers=headers)
			response.raise_for_status()
		except ...

		# Lista de mendicamentos encontrados na página atual
		responseJson = None
		if 'application/json' in response.headers.get('content-type'):
			responseJson = response.json()
#...