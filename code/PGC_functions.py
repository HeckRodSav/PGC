import numpy as np
import cv2
import pytesseract as pt
import matplotlib.pyplot as plt
import os
from math import ceil
import requests
from random_user_agent.user_agent import UserAgent
import unicodedata
import re
import sys
import time
import gc

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

def beep():
	print('\a')
	pass

def plot_img(img, size=10, title=None, cmap='gray'):
	f = plt.figure(figsize=(size,size))
	plt.axis('off')
	if(title != None): plt.title(title)
	_ = plt.imshow(img, cmap=cmap)
	plt.draw()
	plt.pause(0.001)

def plot_array(plot, plot_size = 5, plt_disp=None):
	fig_count = len(plot)
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

def getNowISO():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def sortCriteria(i):
	return (i['rect'][2]//10, len(i['text']), i['rect'][3]//10, -i['cent'][1], i['cent'][0], i['area']//1000, i['conf'], i['text'])




def getWordList(input_img, verb=True, plot_all=False):

	words = []

	data = pt.image_to_data(input_img)

	shape = input_img.shape

	imH, imW = shape[0], shape[1]
	minA = imH * imW // 2500

	lines = data.splitlines()

	index = lines[0].split()
	data = [d.split() for d in lines[1:]]

	table = [ { index[i] : d[i] for i in range(len(d)) } for d in data ]

	aux_img = None
	if plot_all:
		aux_img = input_img.copy()

		if len(shape) == 2:
			aux_img = cv2.cvtColor(input_img,cv2.COLOR_GRAY2RGB)

	if not verb: print('\b-', end='', flush=True)

	for t in table:

		if 'text' not in t: continue
		text = t['text'] # Remove caracteres especiais
		text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
		text = text.encode('ascii', errors='ignore').decode()
		text = ''.join(filter(lambda l: l.isalnum(), text))

		if len(text) <= 0: continue

		# Separar termos CamelCase
		# https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
		textSplit = [w.group(0) for w in re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[a-z])(?=[0-9])|(?<=[0-9])(?=[a-z])|(?<=[0-9])(?=[A-Z])|(?<=[A-Z])(?=[0-9])|(?<=[A-Z])(?=[A-Z][a-z])|$)', text)]
		textRecomposed = ' '.join(textSplit)

		text = text.lower()

		conf = float(t['conf'])

		x, y, w, h = int(t['left']), int(t['top']), int(t['width']), int(t['height'])
		size = w*h

		if conf >= 10 and size >= minA:
			search = {}

			search['text'] = text
			search['area'] = size
			search['conf'] = conf
			search['rect'] = (x, y, w, h)
			search['cent'] = (x+w//2, y+h//2)

			words.append(search)

			if len(textSplit) > 1:
				s = search.copy()
				s['text'] = textRecomposed.lower()
				words.append(s)
				for word in textSplit:
					s = search.copy()
					s['text'] = word.lower()
					words.append(s)
			if plot_all:
				cv2.rectangle(aux_img, (x, y), (x+w, y+h), ((255*(100-conf))//100, (255*(conf))//100, 0), 10)

		elif plot_all: cv2.rectangle(aux_img, (x, y), (x+w, y+h), (0, 0, 0), 1)

	words = sorted(words, key=sortCriteria, reverse=True)

	if verb:
		for t in words:
			print(f"{t['text']:<15}\t{t['conf']}%\t{t['rect'][2]:>4} x {t['rect'][3]:<4} = {t['area']:<6}\tlen:{len(t['text'])}")

	return words, aux_img

def getBoxList(input_img, verb=True, plot_all=False):

	boxes = pt.image_to_boxes(input_img)

	shape = input_img.shape

	imH, imW = shape[0], shape[1]
	lines = boxes.splitlines()

	index = ['c', 'l', 'b', 'r', 't']
	boxes = [l.split() for l in lines]

	table = [ { index[i] : b[i] for i in range(len(index)) } for b in boxes ]

	aux_img = None
	if plot_all:
		aux_img = input_img.copy()

		if len(shape) == 2:
			aux_img = cv2.cvtColor(input_img,cv2.COLOR_GRAY2RGB)

	for t in table:

		char = t['c']

		if char == '~': continue

		l, b, r, t = int(t['l']), int(t['b']), int(t['r']), int(t['t'])

		w, h = (r-l), (t-b)

		size = w * h;

		if verb: print(f"{char}\t\t{w:>4} x {h:<4} = {size:<6}")

		if plot_all:
			cv2.rectangle(aux_img, (l, imH-b), (r, imH-t), (255, 0, 255), 10)

	return table, aux_img






def buscarMedicamento(name, wordList = [], index=None, verbose=True, colorful=False, logFile = None):
	page = 1
	errorMax = 5

	melhorCandidato = {'candidato' : None, 'afinidade' : 0, 'termos' : [], 'sobras':0}

	idx = ''
	if index != None: idx = f' [{index}/{len(wordList)}]'

	while len(name) > 1 and errorMax>0:

		url = f'https://consultas.anvisa.gov.br/api/consulta/bulario?count=100&filter%5BnomeProduto%5D={name}&page={page}'

		# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
		# https://www.w3schools.com/python/python_try_except.asp
		# https://www.geeksforgeeks.org/try-except-else-and-finally-in-python/
		try:
			response = requests.get(url, headers=headers)
			response.raise_for_status()

		except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
			if colorful: print(f'\033[36m', end='')
			print(f'Ocorreu um erro ao buscar "{name}": {e}', flush=True)
			if colorful: print(f'\033[0m', end='')
			print(f'Pausa de 10 segundos', flush=True)
			time.sleep(10)
			print(f'Tentando novamente:', flush=True)
			errorMax -= 1
			continue
		except Exception as e:
			if colorful: print(f'\033[35m', end='')
			print(f'Ocorreu um erro desconhecido ao buscar "{name}": {e}', flush=True)
			if colorful: print(f'\033[0m', end='')
			raise(e)

		responseJson = None
		if 'application/json' in response.headers.get('content-type'):
			responseJson = response.json()

		if responseJson == None or not response.ok or responseJson['totalElements'] <= 0:
			if verbose:
				if colorful: print(f'\033[91m', end='')
				print(f'Sem resultados: {name}{idx}', end='')
				if colorful: print(f'\033[0m', end='')
				print(flush=True)
			break


		for i in range(responseJson['numberOfElements']):

			nomeProduto = responseJson['content'][i]['nomeProduto']
			# Lidar com caraceres especiais
			nomeProduto = ''.join(c for c in unicodedata.normalize('NFD', nomeProduto) if unicodedata.category(c) != 'Mn')
			nomeProduto = nomeProduto.encode('ascii', errors='ignore').decode().lower()

			nameNorm = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
			nameNorm = nameNorm.encode('ascii', errors='ignore').decode().lower()

			if ' ' in name and nameNorm == nomeProduto:
				melhorCandidato['candidato'] = responseJson['content'][i]
				melhorCandidato['afinidade'] = 1
				melhorCandidato['termos'] = [word for word in wordList if word['text'] == name]

				if verbose:
					if colorful: print(f'\033[94m', end='')
					print(f'Candidato promissor: {nomeProduto} <{name}>{idx}\t{"{"}+{melhorCandidato["afinidade"]}-{melhorCandidato["sobras"]}{"}"}', end='')
					if colorful: print(f'\033[0m', end='')
					print(flush=True)


			textSplit = [w.group(0) for w in re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[a-z])(?=[0-9])|(?<=[0-9])(?=[a-z])|(?<=[0-9])(?=[A-Z])|(?<=[A-Z])(?=[0-9])|(?<=[A-Z])(?=[A-Z][a-z])|$)', nomeProduto)]
			nomeProduto = ' '.join(textSplit)
			nomeProdutoTermos = re.split(pattern=r'\ de\ |\ *\+\ *|\ *-\ *|\ +', string=nomeProduto)

			otherWordsList = [w['text'].lower() for w in wordList]

			termos = []

			if len(otherWordsList) > 0 and len(nomeProdutoTermos) > 0 and nameNorm == nomeProdutoTermos[0]:
				some = False

				for termo in nomeProdutoTermos:
					if termo in otherWordsList:
						some = some or True
						termos.append(termo)

				if verbose and not some:
					if colorful: print(f'\033[93m', end='')
					print(f'Candidato errado: {nomeProduto} <{name}>{idx}', end='')
					if colorful: print(f'\033[0m', end='')
					print(flush=True)


			palavras = [word for word in wordList if word['text'] in termos]
			sobras = len(nomeProdutoTermos) - len(palavras)

			if (len(palavras) >= sobras) and ((len(palavras) > melhorCandidato['afinidade']) or (len(palavras) == melhorCandidato['afinidade'] and sobras < melhorCandidato['sobras'])):
				melhorCandidato['candidato'] = responseJson['content'][i]
				melhorCandidato['afinidade'] = len(palavras)
				melhorCandidato['termos'] = palavras
				melhorCandidato['sobras'] = sobras

				if verbose:
					if colorful: print(f'\033[94m', end='')
					print(f'Candidato promissor: {nomeProduto} <{name}>{idx}\t{"{"}+{melhorCandidato["afinidade"]}-{melhorCandidato["sobras"]}{"}"}', end='')
					if colorful: print(f'\033[0m', end='')
					print(flush=True)

			else:

				if verbose:
					if colorful: print(f'\033[93m', end='')
					print(f'Candidato descartado: {nomeProduto} <{name}>{idx}\t{"{"}+{melhorCandidato["afinidade"]}-{melhorCandidato["sobras"]}{"}"}', end='')
					if colorful: print(f'\033[0m', end='')
					print(flush=True)

		if responseJson['last']:
			break
		else:
			page += 1
	else:
		if verbose:
			if errorMax == 0:
				if colorful: print(f'\033[35m', end='')
				print(f'Problema de conexão', end='')
				if colorful: print(f'\033[0m', end='')
				print(flush=True)
			else:
				if colorful: print(f'\033[95m', end='')
				print(f'Ignorando caractere solto: \'{name}\'{idx}', end='')
				if colorful: print(f'\033[0m', end='')
				print(flush=True)


	if melhorCandidato['candidato']:
		if verbose:
			if colorful: print(f'\033[92m', end='')
			print(f'Escolhido: {melhorCandidato["candidato"]["nomeProduto"]}\t<{name}>{idx}\t{"{"}+{melhorCandidato["afinidade"]}-{melhorCandidato["sobras"]}{"}"}', end='')
			if colorful: print(f'\033[0m', end='')
			print(flush=True)
		if logFile: print(f'\nEscolhido: {melhorCandidato["candidato"]["nomeProduto"]}\t<{name}>{idx}\t{"{"}+{melhorCandidato["afinidade"]}-{melhorCandidato["sobras"]}{"}"}\t{getNowISO()}', file=logFile)

	return melhorCandidato['candidato'], melhorCandidato['termos']


def baixarBula(url, nomeComercial, verbose=True, save=True, colorful=True):
	if verbose: print()

	errorMax = 5

	while errorMax > 0:

		try:
			response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
			response.raise_for_status()
			break
		except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
			if colorful: print(f'\033[36m', end='')
			print(f'Ocorreu um erro ao buscar "{nomeComercial}": {e}', flush=True)
			if colorful: print(f'\033[0m', end='')
			print(f'Pausa de 10 segundos', flush=True)
			time.sleep(10)
			print(f'Tentando novamente:', flush=True)
		except Exception as e:
			if colorful: print(f'\033[35m', end='')
			print(f'Ocorreu um erro desconhecido ao buscar "{nomeComercial}": {e}', flush=True)
			if colorful: print(f'\033[0m', end='')
		finally:
			errorMax -= 1
	else:
		if colorful: print(f'\033[35m', end='')
		print(f'Problema de conexão ao buscar "{nomeComercial}"', end='')
		if colorful: print(f'\033[0m', end='')
		print(flush=True)
		return

	nomeDoArquivo = f'{nomeComercial}.pdf'

	if response.ok:
		if verbose:
			if colorful: print(f'\033[32m',end='')
			print(f'Request ok: {nomeDoArquivo}', end='')
			if colorful: print(f'\033[0m',end='')
		if save: open(os.path.join('/mnt/d/Users/HeckRodSav/Downloads/Bulas',nomeDoArquivo),'wb').write(response.content)
		else: print('\t(O arquivo não foi salvo)')
	else:
		if verbose:
			if colorful: print(f'\033[31m',end='')
			print(f'Request error: {response.status_code}', end='')
			if colorful: print(f'\033[0m',end='')
	print()

def testarVariacoes(rgb, check_variants=True, verb_all=True, test_all = True, plot_all = False):

	words_full = {}

	def testAndShow(image, title = '', plot=True, verb=True):
		if verb:
			print()
			print(title)
		else: print('/', end='', flush=True)
		words, img = getWordList(image, verb=verb, plot_all=plot_all)

		if not verb: print('\b\\', end='', flush=True)

		for w in words:
			if(w['text'] not in words_full):
				words_full[w['text']] = w
				words_full[w['text']]['source'] = title
			elif words_full[w['text']]['conf'] > w['conf']:
				words_full[w['text']] = w
				words_full[w['text']]['source'] = title

		if plot:
			array = []
			if(title==''): array.append({'plt':image})
			else: array.append({'plt':image, 'title':title})
			array.append({'plt':img})

			plot_array(array, plot_size = 10, plt_disp=(1,2))
		else: print('\b|', end='', flush=True)

	if test_all: testAndShow(rgb, 'rgb', plot=plot_all, verb=verb_all)

	if check_variants:

		gray = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
		if test_all: testAndShow(gray, 'gray', plot=plot_all, verb=verb_all)

		_, gray_thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		if test_all: testAndShow(gray_thresh, 'gray_thresh', plot=plot_all, verb=verb_all)

		del gray # Liberar memória
		del gray_thresh

		gc.collect()

		rgb_r_only = rgb[...,0].copy()
		rgb_g_only = rgb[...,1].copy()
		rgb_b_only = rgb[...,2].copy()

		if test_all: testAndShow(rgb_r_only,'rgb_r_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(rgb_g_only,'rgb_g_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(rgb_b_only,'rgb_b_only', plot=plot_all, verb=verb_all)


		_, rgb_r_only_thresh = cv2.threshold(rgb_r_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, rgb_g_only_thresh = cv2.threshold(rgb_g_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, rgb_b_only_thresh = cv2.threshold(rgb_b_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

		if test_all: testAndShow(rgb_r_only_thresh,'rgb_r_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(rgb_g_only_thresh,'rgb_g_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(rgb_b_only_thresh,'rgb_b_only_thresh', plot=plot_all, verb=verb_all)


		rgb_tresh = np.dstack((rgb_r_only_thresh, rgb_g_only_thresh, rgb_b_only_thresh))
		if test_all: testAndShow(rgb_tresh,'rgb_tresh', plot=plot_all, verb=verb_all)

		rgb_tresh_gray_thresh = cv2.cvtColor(rgb_tresh,cv2.COLOR_RGB2GRAY)
		if test_all: testAndShow(rgb_tresh_gray_thresh,'rgb_tresh_gray_thresh', plot=plot_all, verb=verb_all)

		del rgb_r_only
		del rgb_g_only
		del rgb_b_only

		del rgb_r_only_thresh
		del rgb_g_only_thresh
		del rgb_b_only_thresh

		del rgb_tresh
		del rgb_tresh_gray_thresh

		gc.collect()


		# https://stackoverflow.com/questions/60814081/how-to-convert-a-rgb-image-into-a-cmyk

		rgb_norm = rgb.astype(np.float64)/255.0

		cmyk_w_only = np.max(rgb_norm, axis=2)

		cmyk_c_only = (np.divide(cmyk_w_only-rgb_norm[...,0], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
		cmyk_m_only = (np.divide(cmyk_w_only-rgb_norm[...,1], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
		cmyk_y_only = (np.divide(cmyk_w_only-rgb_norm[...,2], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
		cmyk_k_only = ((1-cmyk_w_only)*255).astype(np.uint8)

		cmyk = np.dstack((cmyk_c_only,cmyk_m_only,cmyk_y_only,cmyk_k_only))

		if test_all: testAndShow(cmyk_c_only, 'cmyk_c_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_y_only, 'cmyk_y_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_m_only, 'cmyk_m_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_k_only, 'cmyk_k_only', plot=plot_all, verb=verb_all)

		if test_all: testAndShow(cmyk, 'cmyk', plot=plot_all, verb=verb_all)

		_, cmyk_c_only_thresh = cv2.threshold(cmyk_c_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, cmyk_m_only_thresh = cv2.threshold(cmyk_m_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, cmyk_y_only_thresh = cv2.threshold(cmyk_y_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, cmyk_k_only_thresh = cv2.threshold(cmyk_k_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

		cmyk_thresh = np.dstack((cmyk_c_only_thresh,cmyk_m_only_thresh,cmyk_y_only_thresh,cmyk_k_only_thresh))

		if test_all: testAndShow(cmyk_c_only_thresh, 'cmyk_c_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_y_only_thresh, 'cmyk_y_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_m_only_thresh, 'cmyk_m_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(cmyk_k_only_thresh, 'cmyk_k_only_thresh', plot=plot_all, verb=verb_all)

		if test_all: testAndShow(cmyk_thresh, 'cmyk_thresh', plot=plot_all, verb=verb_all)

		r_thresh_recomposed_cmyk = (255*(1-cmyk_c_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)
		g_thresh_recomposed_cmyk = (255*(1-cmyk_m_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)
		b_thresh_recomposed_cmyk = (255*(1-cmyk_y_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)

		rgb_thresh_recomposed_cmyk = np.dstack((r_thresh_recomposed_cmyk, g_thresh_recomposed_cmyk, b_thresh_recomposed_cmyk))
		if test_all: testAndShow(rgb_thresh_recomposed_cmyk, 'rgb_thresh_recomposed_cmyk', plot=plot_all, verb=verb_all)

		del rgb_norm

		del cmyk_w_only

		del cmyk_c_only
		del cmyk_m_only
		del cmyk_y_only
		del cmyk_k_only

		del cmyk

		del cmyk_c_only_thresh
		del cmyk_m_only_thresh
		del cmyk_y_only_thresh
		del cmyk_k_only_thresh

		del cmyk_thresh

		del r_thresh_recomposed_cmyk
		del g_thresh_recomposed_cmyk
		del b_thresh_recomposed_cmyk

		del rgb_thresh_recomposed_cmyk

		gc.collect()


		hls = cv2.cvtColor(rgb,cv2.COLOR_RGB2HLS)
		if test_all: testAndShow(hls, 'hls', plot=plot_all, verb=verb_all)

		hls_h_only = hls[...,0].copy()
		hls_l_only = hls[...,1].copy()
		hls_s_only = hls[...,2].copy()


		if test_all: testAndShow(hls_h_only, 'hls_h_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hls_s_only, 'hls_s_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hls_l_only, 'hls_l_only', plot=plot_all, verb=verb_all)


		_, hls_h_only_thresh = cv2.threshold(hls_h_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, hls_l_only_thresh = cv2.threshold(hls_l_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, hls_s_only_thresh = cv2.threshold(hls_s_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

		if test_all: testAndShow(hls_h_only_thresh,'hls_h_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hls_l_only_thresh,'hls_l_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hls_s_only_thresh,'hls_s_only_thresh', plot=plot_all, verb=verb_all)


		hls_tresh = np.dstack((hls_h_only_thresh, hls_l_only_thresh, hls_s_only_thresh))
		if test_all: testAndShow(hls_tresh,'hls_tresh', plot=plot_all, verb=verb_all)

		rgb_thresh_recomposed_hls = cv2.cvtColor(hls_tresh,cv2.COLOR_HLS2RGB)
		if test_all: testAndShow(rgb_thresh_recomposed_hls, 'rgb_thresh_recomposed_hls', plot=plot_all, verb=verb_all)


		del hls

		del hls_h_only
		del hls_l_only
		del hls_s_only

		del hls_h_only_thresh
		del hls_l_only_thresh
		del hls_s_only_thresh

		del hls_tresh

		del rgb_thresh_recomposed_hls

		gc.collect()


		hsv = cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
		if test_all: testAndShow(hsv, 'hsv', plot=plot_all, verb=verb_all)

		hsv_h_only = hsv[...,0].copy()
		hsv_s_only = hsv[...,1].copy()
		hsv_v_only = hsv[...,2].copy()


		if test_all: testAndShow(hsv_h_only, 'hsv_h_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hsv_s_only, 'hsv_s_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hsv_v_only, 'hsv_v_only', plot=plot_all, verb=verb_all)


		_, hsv_h_only_thresh = cv2.threshold(hsv_h_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, hsv_s_only_thresh = cv2.threshold(hsv_s_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, hsv_v_only_thresh = cv2.threshold(hsv_v_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

		if test_all: testAndShow(hsv_h_only_thresh,'hsv_h_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hsv_s_only_thresh,'hsv_s_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(hsv_v_only_thresh,'hsv_v_only_thresh', plot=plot_all, verb=verb_all)


		hsv_tresh = np.dstack((hsv_h_only_thresh, hsv_s_only_thresh, hsv_v_only_thresh))
		if test_all: testAndShow(hsv_tresh,'hsv_tresh', plot=plot_all, verb=verb_all)

		rgb_thresh_recomposed_hsv = cv2.cvtColor(hsv_tresh,cv2.COLOR_HSV2RGB)
		if test_all: testAndShow(rgb_thresh_recomposed_hsv, 'rgb_thresh_recomposed_hsv', plot=plot_all, verb=verb_all)

		del hsv

		del hsv_h_only
		del hsv_s_only
		del hsv_v_only

		del hsv_h_only_thresh
		del hsv_s_only_thresh
		del hsv_v_only_thresh

		del hsv_tresh

		del rgb_thresh_recomposed_hsv

		gc.collect()


		ycrcb = cv2.cvtColor(rgb,cv2.COLOR_RGB2YCrCb)
		if test_all: testAndShow(ycrcb, 'ycrcb', plot=plot_all, verb=verb_all)

		ycrcb_y_only = ycrcb[...,0].copy()
		ycrcb_cr_only = ycrcb[...,1].copy()
		ycrcb_cb_only = ycrcb[...,2].copy()

		if test_all: testAndShow(ycrcb_y_only, 'ycrcb_y_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(ycrcb_cr_only, 'ycrcb_cr_only', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(ycrcb_cb_only, 'ycrcb_cb_only', plot=plot_all, verb=verb_all)

		_, ycrcb_y_only_thresh = cv2.threshold(ycrcb_y_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, ycrcb_cr_only_thresh = cv2.threshold(ycrcb_cr_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
		_, ycrcb_cb_only_thresh = cv2.threshold(ycrcb_cb_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

		if test_all: testAndShow(ycrcb_y_only_thresh,'ycrcb_y_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(ycrcb_cr_only_thresh,'ycrcb_cr_only_thresh', plot=plot_all, verb=verb_all)
		if test_all: testAndShow(ycrcb_cb_only_thresh,'ycrcb_cb_only_thresh', plot=plot_all, verb=verb_all)


		ycrcb_tresh = np.dstack((ycrcb_y_only_thresh, ycrcb_cr_only_thresh, ycrcb_cb_only_thresh))
		if test_all: testAndShow(ycrcb_tresh,'ycrcb_tresh', plot=plot_all, verb=verb_all)

		rgb_thresh_recomposed_ycrcb = cv2.cvtColor(ycrcb_tresh,cv2.COLOR_YCrCb2RGB)
		if test_all: testAndShow(rgb_thresh_recomposed_ycrcb, 'rgb_thresh_recomposed_ycrcb', plot=plot_all, verb=verb_all)

		del ycrcb

		del ycrcb_y_only
		del ycrcb_cr_only
		del ycrcb_cb_only

		del ycrcb_y_only_thresh
		del ycrcb_cr_only_thresh
		del ycrcb_cb_only_thresh

		del ycrcb_tresh

		del rgb_thresh_recomposed_ycrcb

		gc.collect()


	# Adiciona possíveis variaçõs textuais eliminadas
	word_list_var = {}

	def addVersion(w:str, old:str, new:str):
		if old in w:
			new_w = w.replace(old, new)
			word_list_var[new_w] = words_full[w].copy()
			word_list_var[new_w]['text'] = new_w

	for w in words_full:
		addVersion(w, 'cao', 'ção')
		addVersion(w, 'ao', 'ão')
		addVersion(w, 'ce', 'cê')
		addVersion(w, 'aci', 'áci')

	words_full.update(word_list_var)

	word_list = sorted([words_full[w] for w in words_full], key=sortCriteria, reverse=True)

	return word_list



def pgc(index, img_array_names, logFile = None, check_variants=True, verb_all=False, plot_all=False, test_all=True, plot_middle=False, verb_list=True, online_check=True, baixa_bula=False):

	print('Carregando imagem: ', end=' ', flush=True)

	img_index = img_array_names[index][0]
	img_status = img_array_names[index][1]
	img_name = img_array_names[index][2]
	array_len = len(img_array_names)

	print(f'{img_index} [{index} / {array_len}] "{img_name}"', end = ' ')

	if(logFile): print(f'Carregando imagem: {img_index} [{index} / {array_len}] "{img_name}"\t{getNowISO()}\n', file=logFile)

	rgb = cv2.cvtColor(cv2.imread(os.path.join('./exemplos',img_index)), cv2.COLOR_BGR2RGB)

	shape = rgb.shape
	imH, imW = shape[0], shape[1]
	imA = imH * imW

	print(f'<{imA/1e6 :.3f} Mpx>')

	beep()

	plt.close('all')
	plt.show()

	if plot_middle: plot_img(rgb)

	test_ini = time.time()
	word_list = testarVariacoes(rgb, check_variants=check_variants, verb_all=verb_all, plot_all=plot_all, test_all=test_all)
	test_fin = time.time()

	perf = ((test_fin - test_ini) / imA) * 1e6 # Calculo em mega pixels

	img_name = ''.join(c for c in unicodedata.normalize('NFD', img_name) if unicodedata.category(c) != 'Mn')

	aux_img_name = re.split(pattern=r'\ |-|\+|\ \+\ ', string=img_name.lower())

	print()
	print(f'[{index} - {img_index} - {img_name}]')
	print()
	print(f'Termos encontrados: ({len(word_list)})')

	if(logFile): print(f'Termos encontrados: ({len(word_list)})\t < {perf:.3f} s/Mpx @ {imA/1e6 :.3f} Mpx > \t{getNowISO()}', file=logFile)

	for i, t in enumerate(word_list):
		color_aux = ''
		skipLog = False
		if t['text'].lower() == img_name.lower():
			color_aux = '\u001b[42m'
		elif t['text'].lower() in aux_img_name:
			color_aux = '\u001b[43m'
		elif len(t['text']) == 1:
			color_aux = '\u001b[41m'
			skipLog = True
		if color_aux == '':
			if not verb_list: continue
		else:
			if(logFile) and not skipLog: print(f"<{i:<3}> {t['text']:<15}\t{t['conf']}%\t{t['rect'][2]:>4} x {t['rect'][3]:<4} = {t['area']:<6}\t@({t['cent'][0]},{t['cent'][1]})\tlen:{len(t['text'])}\t source: {t['source']}", file=logFile)
		print(color_aux,end='')
		print(f"<{i:<3}> {t['text']:<15}\t{t['conf']}%\t{t['rect'][2]:>4} x {t['rect'][3]:<4} = {t['area']:<6}\t@({t['cent'][0]},{t['cent'][1]})\tlen:{len(t['text'])}\t source: {t['source']}",end='')
		print(f'\033[0m',end='')
		print()

	escolha = None
	x = y = w = h = None
	termos = []


	if plot_middle:
		all_img = rgb.copy()
		for word in word_list:
			x, y, w, h = word['rect']
			conf = word['conf']
			cv2.rectangle(all_img, (x, y), (x+w, y+h), ((255*(100-conf))//100, (255*(conf))//100, 0), 10)

		array = []
		array.append({'plt':rgb})
		array.append({'plt':all_img})

		plot_array(array, plot_size = 10, plt_disp=(1,2))

	beep()

	if online_check:

		print(img_index, f" [{index} / {array_len}] \"{img_name}\"\n")

		escolha = None

		for idx, word in enumerate(word_list):
			escolha, termos = buscarMedicamento(word['text'], wordList=word_list, index=idx, verbose=True, colorful=True, logFile=logFile)

			if len(termos) > 0: break

		if escolha:

			aux_img = rgb.copy()

			for t in termos:
				x, y, w, h = t['rect']
				cv2.rectangle(aux_img, (x, y), (x+w, y+h), (255, 0, 255), 10)

			codigoBulaPaciente = escolha["idBulaPacienteProtegido"]
			nomeComercial = escolha["nomeProduto"]

			url = f'https://consultas.anvisa.gov.br/api/consulta/medicamentos/arquivo/bula/parecer/{codigoBulaPaciente}/?Authorization='

			print(f'\nURL: {url}')

			if(logFile): print(f'\nURL: {url}', file=logFile)

			if plot_middle:
				array = []
				array.append({'plt':rgb})
				array.append({'plt':aux_img})

				plot_array(array, plot_size = 10, plt_disp=(1,2))

			if baixa_bula:
				baixarBula(url=url, nomeComercial=nomeComercial, verbose=True, save=baixa_bula)

		beep()

	del rgb


	print(img_index, f" [{index} / {array_len}] \"{img_name}\" <{perf:.3f} s/Mpx @ {imA/1e6 :.3f} Mpx >")

	gc.collect()

	return perf






