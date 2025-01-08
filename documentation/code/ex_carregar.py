import cv2 # OpenCV
import os

img_index = img_array_names[index][0] # Recebe nome do arquivo

rgb = cv2.cvtColor(
	cv2.imread(
		os.path.join('./exemplos',img_index)
	),
	cv2.COLOR_BGR2RGB
)