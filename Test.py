import cv2
import numpy as np

img = cv2.imread("M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\frames_extraidos\\frame_0037.png")
img= cv2.resize(img, (700, 425))


imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("image", imghsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

pixel1 = imghsv[10,400]
pixel2 = imghsv[10,424]
pixel3 = imghsv[300,400]
pixel4 = imghsv[300,424]
print(pixel1)
print(pixel2)
print(pixel3)
print(pixel4)

lower_red = np.array([168, 50, 124])
upper_red = np.array([198, 255, 255])
mask = cv2.inRange(imghsv, lower_red, upper_red)

cv2.imshow("image", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = np.ones((3, 3), np.uint8)
dilatacion = cv2.erode(255-mask, kernel, iterations = 9)
erosion = cv2.dilate(dilatacion, kernel, iterations = 9)
mask = erosion

cv2.imshow("image", dilatacion)
cv2.waitKey(0)
cv2.destroyAllWindows()

pelota = cv2.bitwise_or(img, img, mask=255-mask)
cv2.imshow("image", pelota)
cv2.waitKey(0)
cv2.destroyAllWindows()




