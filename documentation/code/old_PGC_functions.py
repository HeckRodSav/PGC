import numpy as np
import cv2
import pytesseract as pt
# from google.colab.patches import cv2_imshow # for image display
import matplotlib.pyplot as plt
import os
from math import ceil
import requests
import json
from random_user_agent.user_agent import UserAgent

# Play an audio beep. Any audio URL will do.
# from google.colab import output
def beep():
	# # output.eval_js('new Audio("https://upload.wikimedia.org/wikipedia/commons/0/05/Beep-09.ogg").play()')
	# output.eval_js('new Audio("https://upload.wikimedia.org/wikipedia/commons/6/61/Beep_400ms.ogg").play()')
	print('\a')
	pass

def plot_img(img, size=10, title=None, cmap='gray'):
	# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Necessário para imagem aparecer corretamente
	plt.figure(figsize=(size,size))
	plt.axis('off')
	if(title != None): plt.title(title)
	_ = plt.imshow(img, cmap=cmap)
	plt.draw()
	plt.pause(0.001)

def plot_array(plot, plot_size = 5, plt_disp=None):
	fig_count = len(plot)
	# plt_disp = (1,fig_count)
	side = ceil(fig_count**0.5)
	if not plt_disp or plt_disp[0]*plt_disp[1] < fig_count:
		plt_disp = (side,side)
	plt.figure(figsize=(plot_size*plt_disp[1], plot_size*plt_disp[0]))

	for i,img in enumerate(plot):
		plt.subplot(*plt_disp, i+1)
		plt.axis('off')
		if not 'cmap' in img:
			img['cmap'] = 'gray'
		plt.imshow(img['plt'],img['cmap'])
		if 'title' in img: plt.title(img['title'])
	plt.draw()
	plt.pause(0.001)
	# plt.show()

def getWordList(input_img):

	words = []

	# string = pt.image_to_string(input_img)

	# print(string)

	# boxes = pt.image_to_boxes(input_img)
	data = pt.image_to_data(input_img)

	shape = input_img.shape

	imH, imW = shape[0], shape[1]
	lines = data.splitlines()

	index = lines[0].split()
	data = [d.split() for d in lines[1:]]

	table = [ { index[i] : d[i] for i in range(len(d)) } for d in data ]

	# print(index)

	aux_img = input_img.copy()

	if len(shape) == 2:
		aux_img = cv2.cvtColor(input_img,cv2.COLOR_GRAY2RGB)


	for t in table:

		if 'text' not in t: continue
		text = ''.join(filter(lambda l: l.isalnum(), t['text'])) # Remove caracteres especiais

		if len(text) < 3: continue

		conf = float(t['conf'])

		x, y, w, h = int(t['left']), int(t['top']), int(t['width']), int(t['height'])

		if conf >= 10:
			size = w*h
			search = {}

			search['text'] = text
			search['size'] = size
			search['conf'] = conf
			search['rect'] = (x, y, w, h)

			words.append(search)

			print(f"{text}\t{t['conf']}%\t{w} x {h} = {size}\tlen:{len(text)}")

			cv2.rectangle(aux_img, (x, y), (x+w, y+h), ((255*(100-conf))//100, (255*(conf))//100, 0), 10)

			# print(t)
		else: cv2.rectangle(aux_img, (x, y), (x+w, y+h), (0, 0, 0), 1)

	words = sorted(words, key=lambda i: (i['size'], i['conf'], len(i['text']), i['text']), reverse=True)

	return words, aux_img

headers = { # De https://github.com/iuryLandin/bulario/blob/main/src/bulario.js
	"accept": "application/json, text/plain, */*",
	"accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
	"authorization": "Guest",
	"cache-control": "no-cache",
	"if-modified-since": "Mon, 26 Jul 1997 05:00:00 GMT",
	"pragma": "no-cache",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "\"Windows\"",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"cookie": "FGTServer=77E1DC77AE2F953D7ED796A08A630A01A53CF6FE5FD0E106412591871F9A9BBCFBDEA0AD564FD89D3BDE8278200B; FGTServer=77E1DC77AE2F953D7ED796A08A630A01A53CF6FE5FD0E106412591871F9A9BBCFBDEA0AD564FD89D3BDE8278200B; FGTServer=77E1DC77AE2F953D7ED796A08A630A01A53CF6FE5FD0E106412591871F9A9BBCFBDEA0AD564FD89D3BDE8278200B; _pk_id.42.210e=8eca716434ce3237.1690380888.; FGTServer=77E1DC77AE2F953D7ED796A08A630A01A53CF6FE5FD0E106412591871F9A9BBCFBDEA0AD564FD89D3BDE8278200B; _cfuvid=L.SzxLLxZoWYrYqhaiRgS5MTkV77mwE5uIyLNWvyufk-1690462598410-0-604800000; _pk_ref.42.210e=%5B%22%22%2C%22%22%2C1690462669%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.42.210e=1; cf_clearance=tk5QcLSYPlUQfr8s2bTGXyvC2KZdHcEIYU8r6HCgNvQ-1690462689-0-160.0.0",
	"Referer": "https://consultas.anvisa.gov.br/",
	"UserAgent": UserAgent().get_random_user_agent(),
	"Referrer-Policy": "no-referrer-when-downgrade"
}

def buscarMedicamento(name, page=1, verbose=True):
	# response = requests.get(f'https://bula.vercel.app/pesquisar?nome={name}&pagina=1', timeout=5)
	response = requests.get(f'https://consultas.anvisa.gov.br/api/consulta/bulario?count=10&filter%5BnomeProduto%5D={name}&page={page}', headers=headers)
	# response = requests.request(method='GET',url=f'https://consultas.anvisa.gov.br/api/consulta/bulario?count=10&filter%5BnomeProduto%5D={name}&page={page}', headers=headers)
	responseJson = response.json()
	# print(responseJson)
	if not response.ok or responseJson["totalElements"] <= 0:
		if verbose: print(f'Não encontrado: {name}')
		return None
	else:
		nomeProduto = responseJson['content'][0]['nomeProduto']
		if nomeProduto.upper() != name.upper():
			if verbose: print(f"Candidato errado: ({name.upper()}) {nomeProduto}")
			return None
		else:
			if verbose: print(f'Encontrado: {name}')
			return responseJson

def buscaInformacoes(numProcesso):
	# response = requests.get(f"https://bula.vercel.app/medicamento/{numProcesso}", timeout=5)
	response = requests.get(f"https://consultas.anvisa.gov.br/api/consulta/medicamento/produtos/{numProcesso}", timeout=5, headers=headers)

	return response.json() if response.ok else None

def getBula(input_img, skip_set = set(), show_img=False, verbose=True):
	url, nomeComercial = None, None
	words, img = getWordList(input_img)

	words = filter(lambda w: w['text'] not in skip_set, words) # Remover palavras já analisadas

	escolha = None
	x = y = w = h = None

	for word in words:
		escolha = buscarMedicamento(word['text'])

		if escolha:
			x, y, w, h = word['rect']
			break
		else: skip_set.add(word['text'])

	if escolha:

		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 127, 255), 10)

		if verbose: print(json.dumps(escolha, indent=2))

		numProcesso = escolha["content"][0]["numProcesso"]

		informacoes = buscaInformacoes(numProcesso)

		if informacoes:
			if verbose: print(json.dumps(informacoes, indent=2))

			codigoBulaPaciente = informacoes["codigoBulaPaciente"]
			nomeComercial = informacoes["nomeComercial"]

			url = f'https://consultas.anvisa.gov.br/api/consulta/medicamentos/arquivo/bula/parecer/{codigoBulaPaciente}/?Authorization='

	if show_img:
		array = []
		array.append({'plt':input_img})
		array.append({'plt':img})

		plot_array(array, plot_size = 10, plt_disp=(1,2))

	return url, nomeComercial, img, skip_set

def baixarBula(url, nomeComercial, verbose=True):
	if verbose: print(url)
	r = requests.get(url, allow_redirects=True, timeout=5)
	if verbose: print('r', *r)
	if r.ok:
		if verbose: print("Request ok")
		open(f'{nomeComercial}.pdf','wb').write(r.content)
	else:
		if verbose: print(f"Request error: {r.status_code}")

def tryGrayBula(input_img, skip_set):
	gray_img = cv2.cvtColor(input_img,cv2.COLOR_RGB2GRAY)
	url, nomeComercial, img, new_skip_set = getBula(gray_img, show_img=True, verbose=False)
	skip_set.union(new_skip_set)
	return gray_img, url, nomeComercial, img, skip_set

def tryThreshBula(input_img, skip_set):
	_, thresh_img = cv2.threshold(input_img,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
	url, nomeComercial, img, new_skip_set = getBula(thresh_img, show_img=True, verbose=False)
	skip_set.union(new_skip_set)
	return thresh_img, url, nomeComercial, img, skip_set

def testarVariacoes(input_img, verbose=True):
	skip_set = set()


	# RAW
	if verbose: print('RAW')
	url, nomeComercial, img, new_skip_set = getBula(input_img, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# Gray
	if verbose: print('Gray')
	gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(input_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# Gray thresh
	if verbose: print('Gray thresh')
	gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# R only
	if verbose: print('R only')
	r_only_img = input_img[:,:,0].copy()
	url, nomeComercial, img, new_skip_set = getBula(r_only_img, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# R only thresh
	if verbose: print('R only thresh')
	r_only_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(r_only_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# G only
	if verbose: print('G only')
	g_only_img = input_img[:,:,1].copy()
	url, nomeComercial, img, new_skip_set = getBula(g_only_img, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# G only thresh
	if verbose: print('G only thresh')
	g_only_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(g_only_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# B only
	if verbose: print('B only')
	b_only_img = input_img[:,:,2].copy()
	url, nomeComercial, img, new_skip_set = getBula(b_only_img, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# B only thresh
	if verbose: print('B only thresh')
	b_only_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(b_only_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# RGB thresh
	if verbose: print('RGB thresh')
	rgb_tresh_img = np.zeros(input_img.shape, dtype=np.uint8)
	rgb_tresh_img[:,:,0] = r_only_thresh_img
	rgb_tresh_img[:,:,1] = g_only_thresh_img
	rgb_tresh_img[:,:,2] = b_only_thresh_img
	url, nomeComercial, img, new_skip_set = getBula(rgb_tresh_img, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)


	# RGB thresh Gray
	if verbose: print('RGB thresh Gray')
	rgb_tresh_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(rgb_tresh_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# RGB thresh Gray thresh
	if verbose: print('RGB thresh Gray thresh')
	rgb_tresh_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(rgb_tresh_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)




	# R shadow
	if verbose: print('R shadow')
	r_shadow = input_img.copy()
	r_shadow[:, :, 1] = 0
	r_shadow[:, :, 2] = 0
	url, nomeComercial, img, new_skip_set = getBula(r_shadow, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# R shadow Gray
	if verbose: print('R shadow Gray')

	r_shadow_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(r_shadow, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# R shadow Gray thresh
	if verbose: print('R shadow Gray thresh')
	r_shadow_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(r_shadow_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)




	# R light
	if verbose: print('R light')
	r_light = input_img.copy()
	r_light[:, :, 1] = 255
	r_light[:, :, 2] = 255
	url, nomeComercial, img, new_skip_set = getBula(r_light, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# R light Gray
	if verbose: print('R light Gray')

	r_light_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(r_light, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# R light Gray thresh
	if verbose: print('R light Gray thresh')
	r_light_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(r_light_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)



	# G shadow
	if verbose: print('G shadow')
	g_shadow = input_img.copy()
	g_shadow[:, :, 0] = 0
	g_shadow[:, :, 2] = 0
	url, nomeComercial, img, new_skip_set = getBula(g_shadow, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# G shadow Gray
	if verbose: print('G shadow Gray')

	g_shadow_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(g_shadow, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# G shadow Gray thresh
	if verbose: print('G shadow Gray thresh')
	g_shadow_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(g_shadow_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)





	# G light
	if verbose: print('G light')
	g_light = input_img.copy()
	g_light[:, :, 0] = 255
	g_light[:, :, 2] = 255
	url, nomeComercial, img, new_skip_set = getBula(g_light, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# G light Gray
	if verbose: print('G light Gray')

	g_light_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(g_light, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# G light Gray thresh
	if verbose: print('G light Gray thresh')
	g_light_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(g_light_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)



	# B shadow
	if verbose: print('B shadow')
	b_shadow = input_img.copy()
	b_shadow[:, :, 1] = 0
	b_shadow[:, :, 0] = 0
	url, nomeComercial, img, new_skip_set = getBula(b_shadow, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# B shadow Gray
	if verbose: print('B shadow Gray')

	b_shadow_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(b_shadow, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# B shadow Gray thresh
	if verbose: print('B shadow Gray thresh')
	b_shadow_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(b_shadow_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)




	# B light
	if verbose: print('B light')
	b_light = input_img.copy()
	b_light[:, :, 1] = 255
	b_light[:, :, 0] = 255
	url, nomeComercial, img, new_skip_set = getBula(b_light, show_img=True, verbose=False)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# B light Gray
	if verbose: print('B light Gray')

	b_light_gray_img, url, nomeComercial, img, new_skip_set = tryGrayBula(b_light, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	# B light Gray thresh
	if verbose: print('B light Gray thresh')
	b_light_gray_thresh_img, url, nomeComercial, img, new_skip_set = tryThreshBula(b_light_gray_img, skip_set)
	if url: return url, nomeComercial
	skip_set.union(new_skip_set)

	return None
