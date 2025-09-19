import cv2

#Se ejecuta cuando haces clic en la imagen y muestra las coordenadas de la posición clickeada
def mostrar_posicion(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: #Click izquierdo
        print(f"Posición: x={x}, y={y}")

        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow("Imagen", img)

#Carga la imagen
img = cv2.imread("M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\frames_extraidos\\frame_0020.png")
img= cv2.resize(img, (700, 425))

cv2.imshow("Imagen", img)
cv2.setMouseCallback("Imagen", mostrar_posicion)

cv2.waitKey(0)
cv2.destroyAllWindows()
