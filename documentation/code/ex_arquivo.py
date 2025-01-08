def baixarBula(url, nomeComercial, save=True):
	errorMax = 5

	while errorMax > 0:
		try:
			response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
			response.raise_for_status()
			break
		except ...
		finally:
			errorMax -= 1
	else: return

	nomeDoArquivo = f'{nomeComercial}.pdf'

	if response.ok:
		if save: open(os.path.join('/mnt/d/Users/HeckRodSav/Downloads/Bulas',nomeDoArquivo),'wb').write(response.content)



escolha = None

for idx, word in enumerate(word_list):
	escolha, termos = buscarMedicamento(word['text'], wordList=word_list, ...)
	if len(termos) > 0: break

if escolha:

	codigoBulaPaciente = escolha["idBulaPacienteProtegido"]
	nomeComercial = escolha["nomeProduto"]

	url = f'https://consultas.anvisa.gov.br/api/consulta/medicamentos/arquivo/bula/parecer/{codigoBulaPaciente}/?Authorization='

	baixarBula(url=url, nomeComercial=nomeComercial)
