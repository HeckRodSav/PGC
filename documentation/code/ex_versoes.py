words_full = {}

def testAndShow(image, title = '', plot=True, verb=True):
	words, img = getWordList(image, verb=verb)

	for w in words:
		if(w['text'] not in words_full):
			words_full[w['text']] = w
			words_full[w['text']]['source'] = title

gray = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
testAndShow(gray, 'gray')

_, gray_thresh = cv2.threshold(
	gray, 0, 255,
	cv2.THRESH_OTSU + cv2.THRESH_BINARY
)
testAndShow(gray_thresh, 'gray_thresh')

del gray # Liberar memória
del gray_thresh

rgb_r_only = rgb[...,0].copy()
rgb_g_only = rgb[...,1].copy()
rgb_b_only = rgb[...,2].copy()

testAndShow(rgb_r_only,'rgb_r_only')
testAndShow(rgb_g_only,'rgb_g_only')
testAndShow(rgb_b_only,'rgb_b_only')

# ...