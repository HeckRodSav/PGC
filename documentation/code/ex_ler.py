import pytesseract as pt

def getWordList(input_img, verb=True):

	words = []

	data = pt.image_to_data(input_img)
	lines = data.splitlines()
	index = lines[0].split()
	data = [d.split() for d in lines[1:]]

	table = [
		{
			index[i] : d[i] for i in range(len(d))
		} for d in data
	]

	#...