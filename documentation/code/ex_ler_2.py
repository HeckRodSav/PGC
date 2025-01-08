#...
	shape = input_img.shape
	imH, imW = shape[0], shape[1]
	minA = imH * imW // 2500 # Área mínima

	for t in table: # Percorre lista de palavras encontradas

		if 'text' not in t: continue

		text = t['text'] # Remove caracteres especiais
		#...

		conf = float(t['conf'])

		x, y = int(t['left']), int(t['top'])
		w, h = int(t['width']), int(t['height'])
		size = w*h

		if conf >= 10 and size >= minA:
			search = {}

			search['text'] = text
			search['area'] = size
			search['conf'] = conf
			search['rect'] = (x, y, w, h)
			search['cent'] = (x+w//2, y+h//2)

			words.append(search)

	words = sorted(words, key=sortCriteria, reverse=True)

	return words, aux_img