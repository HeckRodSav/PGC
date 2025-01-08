def sortCriteria(item):
	return (
		item['rect'][2]//10,
		len(item['text']),
		item['rect'][3]//10,
		-item['cent'][1],
		item['cent'][0],
		item['area']//1000,
		item['conf'],
		item['text']
	)

word_list = sorted(
	[words_full[w] for w in words_full],
	key=sortCriteria,
	reverse=True
)