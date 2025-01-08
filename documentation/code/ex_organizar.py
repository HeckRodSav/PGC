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