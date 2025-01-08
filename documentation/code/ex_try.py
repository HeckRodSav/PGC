errorMax = 5

while errorMax>0:

	try:
		response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
		response.raise_for_status()
		break
	except (
			requests.exceptions.ReadTimeout,
			requests.exceptions.HTTPError,
			requests.exceptions.ConnectionError
		) as e:

		# Exibir mensagem de erro específica

	except Exception as e:

		# Exibir mensagem de erro geral

	finally:
		errorMax -= 1