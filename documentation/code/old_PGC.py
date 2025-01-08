from PGC_functions import *


img_array_names = [
	# 'IMG_20210707_102647.jpg', # Janssen COVID-19 Vaccine
	# 'IMG_20220908_191849.jpg', # Neopiridin
	'IMG_20230726_092806.jpg', # tysabri
	# 'IMG_20230909_211815.jpg', #
	# 'IMG_20230910_124309.jpg', # Dipirona monoidratada
	'IMG_20230918_111341.jpg', # Magnazia
	'IMG_20230918_111346.jpg', # Aubagio
	# 'IMG_20230918_111401.jpg', #
	'IMG_20231031_143050.jpg', # ciprofibrato
	# 'IMG_20231031_143056.jpg', # atorvastatina cálcina
	'IMG_20231031_143122.jpg', # enterogermina
	'IMG_20231031_143205.jpg', # Fluive
	# 'IMG_20231031_143239.jpg', # cloridrato de metformina
	# 'IMG_20231031_143358.jpg', # Loratamed
	# 'IMG_20231031_143405.jpg', #
	# 'IMG_20231031_143425.jpg', # Venvanse
	'IMG_20231031_143519.jpg', # Betacortazol
	'IMG_20231031_143541.jpg', # simeticona
	'IMG_20231031_143607.jpg', # sosseg
	'IMG_20231031_143629.jpg', # Venvanse
	# 'IMG_20231031_143647.jpg', # losartana potássica
	'IMG_20231031_143702.jpg', # hidroclorotiazida
	# 'IMG_20231031_143720.jpg', # Florent
	'IMG_20231031_143816.jpg', # Neosoro
	# 'IMG_20231031_143831.jpg', # narix
	'IMG_20231031_143918.jpg', # Buprovil
	'IMG_20231031_143954.jpg', # queimalive
	'IMG_20231102_210230.jpg', # Advil
	'IMG_20231108_143053.jpg', # Simeticon
	# 'IMG_20231108_143121.jpg', #
	# 'IMG_20231108_143142.jpg', #
	'IMG_20231108_143237.jpg', # dauf
	'IMG_20231108_143533.jpg', # ENO
	'IMG_20231108_144934.jpg', # Pondicilina
	'IMG_20231109_154156.jpg', # Naldecon
	'IMG_20231109_154215.jpg', # dipirona monoidratada
]


img_array = { img_name : cv2.cvtColor(cv2.imread(os.path.join('./exemplos',img_name)), cv2.COLOR_BGR2RGB) for img_name in img_array_names }

plt.show()

# for i, img_idx in enumerate(img_array):
# 	print(i, ':', img_idx)
# 	# plt.ioff()
# 	plot_img(img_array[img_idx], 5, title=f'{i}:{img_idx}')

# # plt.show()

beep()

input("Enter para continuar")

plt.close('all')
plt.show()

img_index = img_array_names[16]
input_img = img_array[img_index]
# plot_img(input_img, size=5, title=img_index)
# words, img = getWordList(input_img)
# print(words)

# url, nomeComercial, img, skip_list = getBula(input_img)
# print(nomeComercial)
# print(url)
# print(skip_list)
# plot_img(img, size=5, title=nomeComercial)

ret = testarVariacoes(input_img)
print(ret)
beep()


input("Enter para encerrar")
