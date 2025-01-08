#!/usr/bin/python3

from PGC_functions import *

from image_list import img_array_names_filtered as img_array_names

import json

# img_array_names = [n for n in img_array_names if (n[1] & 0b0011) == 0b0010 and (n[1] & 0b1100) > 0b0100]
# img_array_names = [n for n in img_array_names if not (n[1] & 0b0011) == 0b0001 and (n[1] & 0b0111) >= 0b0100 or n[1] == 0b0000]
# img_array_names = [n for n in img_array_names if n[1] == 0b0000]

img_array_names = [ img_array_names [0] ]

# print(*img_array_names, sep='\n')
# print()
# print(len(img_array_names), sep='\n')

# print(buscarMedicamento('benatux'))
# buscarMedicamentoAlt('dipirona')

# for i, t in enumerate(img_array_names):
# 	print(i, t, sep='\t')
# print()
# print(len(img_array_names), sep='\n')

# aux = {}
# for i in img_array_names:
# 	aux[i[0]] = {'name':i[2]}

# print(json.dumps(aux, indent=4, separators=(',', ':')))


def showBoxes_aux(input_img):

	data = pt.image_to_data(input_img)

	shape = input_img.shape

	imH, imW = shape[0], shape[1]
	minA = imH * imW // 2500

	lines = data.splitlines()

	index = lines[0].split()
	data = [d.split() for d in lines[1:]]

	table = [ { index[i] : d[i] for i in range(len(d)) } for d in data ]

	aux_img = None
	# if plot_all:
	aux_img = input_img.copy()

	if len(shape) < 3:
		aux_img = cv2.cvtColor(input_img,cv2.COLOR_GRAY2RGB)

	for t in table:

		if 'text' not in t: continue
		text = t['text'] # Remove caracteres especiais
		text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
		text = text.encode('ascii', errors='ignore').decode()
		text = ''.join(filter(lambda l: l.isalnum(), text))

		if len(text) <= 0: continue

		conf = float(t['conf'])

		x, y, w, h = int(t['left']), int(t['top']), int(t['width']), int(t['height'])
		size = w*h

		if conf >= 10 and size >= minA:
			cv2.rectangle(aux_img, (x, y), (x+w, y+h), ((255*(100-conf))//100, (255*(conf))//100, 0), 10)

		else:
			cv2.rectangle(aux_img, (x, y), (x+w, y+h), (0, 0, 0), 1)


	if (len(shape) == 2) or (len(shape) > 2 and shape[2] < 4):
		aux_img = cv2.cvtColor(aux_img, cv2.COLOR_RGB2BGR)

	return aux_img



# import signal
# from time import sleep

# keepGoing = True

# def sigQuitF(signal, frame):
# 	print(signal, flush=True)
# 	global keepGoing
# 	if not keepGoing: exit(0)
# 	keepGoing = False

# signal.signal( signal.SIGINT, sigQuitF)


# while True:
# 	print(keepGoing)
# 	sleep(1)

# import time

# t = time.time()

# print(time.strftime('%Y-%m-%d_%H:%M:%S.log', time.localtime(t)))

img_index = img_array_names[0][0]
img_name = img_array_names[0][2]

local_aux = './presentation/'+img_name

print(img_name)

bgr = cv2.imread(os.path.join('./exemplos',img_index))
# cv2.imwrite(local_aux+'_rgb.jpg', bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
# cv2.imwrite(local_aux+'_bgr.jpg', rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
# cv2.imwrite(local_aux+'_rgb_boxes.jpg', showBoxes_aux(rgb), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

del bgr
gc.collect()

HLS = cv2.cvtColor(rgb, cv2.COLOR_RGB2HLS)
HSV = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
YCrCb = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)

cv2.imwrite(local_aux+'_HLS.jpg', cv2.cvtColor(HLS, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_HSV.jpg', cv2.cvtColor(HSV, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_YCrCb.jpg', cv2.cvtColor(YCrCb, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

exit(0)


gray = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
cv2.imwrite(local_aux+'_gray.jpg', gray, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_gray_boxes.jpg', showBoxes_aux(gray), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)


_, gray_thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
cv2.imwrite(local_aux+'_gray_thresh.jpg', gray_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_gray_thresh_boxes.jpg', showBoxes_aux(gray_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

del gray
del gray_thresh
gc.collect()

rgb_r_only = rgb[...,0].copy()
rgb_g_only = rgb[...,1].copy()
rgb_b_only = rgb[...,2].copy()

cv2.imwrite(local_aux+'_rgb_r_only.jpg', rgb_r_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_g_only.jpg', rgb_g_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_b_only.jpg', rgb_b_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_r_only_boxes.jpg', showBoxes_aux(rgb_r_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_g_only_boxes.jpg', showBoxes_aux(rgb_g_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_b_only_boxes.jpg', showBoxes_aux(rgb_b_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)


_, rgb_r_only_thresh = cv2.threshold(rgb_r_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
_, rgb_g_only_thresh = cv2.threshold(rgb_g_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
_, rgb_b_only_thresh = cv2.threshold(rgb_b_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

del rgb_r_only
del rgb_g_only
del rgb_b_only

gc.collect()

cv2.imwrite(local_aux+'_rgb_r_only_thresh.jpg', rgb_r_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_g_only_thresh.jpg', rgb_g_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_b_only_thresh.jpg', rgb_b_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_r_only_thresh_boxes.jpg', showBoxes_aux(rgb_r_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_g_only_thresh_boxes.jpg', showBoxes_aux(rgb_g_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_b_only_thresh_boxes.jpg', showBoxes_aux(rgb_b_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

rgb_thresh = np.dstack((rgb_r_only_thresh, rgb_g_only_thresh, rgb_b_only_thresh))

del rgb_r_only_thresh
del rgb_g_only_thresh
del rgb_b_only_thresh

gc.collect()

cv2.imwrite(local_aux+'_rgb_thresh.jpg', cv2.cvtColor(rgb_thresh, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_thresh_boxes.jpg', showBoxes_aux(rgb_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)


rgb_thresh_gray_thresh = cv2.cvtColor(rgb_thresh,cv2.COLOR_RGB2GRAY)
cv2.imwrite(local_aux+'_rgb_thresh_gray_thresh.jpg', rgb_thresh_gray_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_thresh_gray_thresh_boxes.jpg', showBoxes_aux(rgb_thresh_gray_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

del rgb_thresh
del rgb_thresh_gray_thresh
gc.collect()

rgb_norm = rgb.astype(np.float64)/255.0

cmyk_w_only = np.max(rgb_norm, axis=2)

cmyk_c_only = (np.divide(cmyk_w_only-rgb_norm[...,0], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
cmyk_m_only = (np.divide(cmyk_w_only-rgb_norm[...,1], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
cmyk_y_only = (np.divide(cmyk_w_only-rgb_norm[...,2], cmyk_w_only, where=cmyk_w_only!=0)*255).astype(np.uint8)
cmyk_k_only = ((1-cmyk_w_only)*255).astype(np.uint8)

del rgb_norm
gc.collect()

cv2.imwrite(local_aux+'_cmyk_c_only.jpg', cmyk_c_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_m_only.jpg', cmyk_m_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_y_only.jpg', cmyk_y_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_k_only.jpg', cmyk_k_only, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

cv2.imwrite(local_aux+'_cmyk_c_only_boxes.jpg', showBoxes_aux(cmyk_c_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_m_only_boxes.jpg', showBoxes_aux(cmyk_m_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_y_only_boxes.jpg', showBoxes_aux(cmyk_y_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_k_only_boxes.jpg', showBoxes_aux(cmyk_k_only), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)



cmyk = np.dstack((cmyk_c_only,cmyk_m_only,cmyk_y_only,cmyk_k_only))

cv2.imwrite(local_aux+'_cmyk.jpg', cmyk, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_boxes.jpg', showBoxes_aux(cmyk), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

_, cmyk_c_only_thresh = cv2.threshold(cmyk_c_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
_, cmyk_m_only_thresh = cv2.threshold(cmyk_m_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
_, cmyk_y_only_thresh = cv2.threshold(cmyk_y_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
_, cmyk_k_only_thresh = cv2.threshold(cmyk_k_only,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)

del cmyk_c_only
del cmyk_m_only
del cmyk_y_only
del cmyk_k_only
gc.collect()

cv2.imwrite(local_aux+'_cmyk_c_only_thresh.jpg', cmyk_c_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_m_only_thresh.jpg', cmyk_m_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_y_only_thresh.jpg', cmyk_y_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_k_only_thresh.jpg', cmyk_k_only_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_c_only_thresh_boxes.jpg', showBoxes_aux(cmyk_c_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_m_only_thresh_boxes.jpg', showBoxes_aux(cmyk_m_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_y_only_thresh_boxes.jpg', showBoxes_aux(cmyk_y_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_k_only_thresh_boxes.jpg', showBoxes_aux(cmyk_k_only_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)


cmyk_thresh = np.dstack((cmyk_c_only_thresh,cmyk_m_only_thresh,cmyk_y_only_thresh,cmyk_k_only_thresh))

cv2.imwrite(local_aux+'_cmyk_thresh.jpg', cmyk_thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_cmyk_thresh_boxes.jpg', showBoxes_aux(cmyk_thresh), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

r_thresh_recomposed_cmyk = (255*(1-cmyk_c_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)
g_thresh_recomposed_cmyk = (255*(1-cmyk_m_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)
b_thresh_recomposed_cmyk = (255*(1-cmyk_y_only_thresh/255.0)*(1-cmyk_k_only_thresh/255.0)).astype(np.uint8)

del cmyk_c_only_thresh
del cmyk_m_only_thresh
del cmyk_y_only_thresh
del cmyk_k_only_thresh

gc.collect()

cv2.imwrite(local_aux+'_r_thresh_recomposed_cmyk.jpg', r_thresh_recomposed_cmyk, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_g_thresh_recomposed_cmyk.jpg', g_thresh_recomposed_cmyk, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_b_thresh_recomposed_cmyk.jpg', b_thresh_recomposed_cmyk, [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

cv2.imwrite(local_aux+'_r_thresh_recomposed_cmyk_boxes.jpg', showBoxes_aux(r_thresh_recomposed_cmyk), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_g_thresh_recomposed_cmyk_boxes.jpg', showBoxes_aux(g_thresh_recomposed_cmyk), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_b_thresh_recomposed_cmyk_boxes.jpg', showBoxes_aux(b_thresh_recomposed_cmyk), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

rgb_thresh_recomposed_cmyk = np.dstack((r_thresh_recomposed_cmyk, g_thresh_recomposed_cmyk, b_thresh_recomposed_cmyk))

cv2.imwrite(local_aux+'_rgb_thresh_recomposed_cmyk.jpg', cv2.cvtColor(rgb_thresh_recomposed_cmyk,cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)
cv2.imwrite(local_aux+'_rgb_thresh_recomposed_cmyk_boxes.jpg', showBoxes_aux(rgb_thresh_recomposed_cmyk), [int(cv2.IMWRITE_JPEG_QUALITY), 90]); print('.', end='', flush=True)

print('\a')