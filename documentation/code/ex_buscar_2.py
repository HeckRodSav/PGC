#...
		for i in range(responseJson['numberOfElements']):

			nomeProduto = responseJson['content'][i]['nomeProduto'] # Lidar com caraceres especiais
			# ...

			#  Partes do nome do medicamento
			nomeProdutoTermos = re.split(pattern=r'\ de\ |\ *\+\ *|\ *-\ *|\ +', string=nomeProduto)

			# Demais termos encontrados na imagem
			otherWordsList = [w['text'].lower() for w in wordList]

			termos = []
			for termo in nomeProdutoTermos:
				if termo in otherWordsList: # Termo compatível
					termos.append(termo)

			palavras = [word for word in wordList if word['text'] in termos]
			sobras = len(nomeProdutoTermos) - len(palavras)

			# Atualizar melhorCandidato
			if len(palavras) > melhorCandidato['afinidade']:
				# Atualizar melhorCandidato

		if responseJson['last']: break
		else: page += 1 # Próxima página
	return melhorCandidato['candidato'],
		melhorCandidato['termos']
