import cv2
import numpy as np

#Parametros para pausar el video
pausar_video = False
mostrar_pixel = False

#Ejecuta la funcion de mostrar el color del pixel seleccionado o pausar el video
def mouse_callback(event, _x, _y, flags, param):
    global pausar_video, mostrar_pixel, x, y
    if event == cv2.EVENT_LBUTTONDOWN: #Click izquierdo mostrar color pixel
        x, y = _x, _y
        mostrar_pixel = True
    if event == cv2.EVENT_RBUTTONDOWN: #Click derecho mostrar color pixel
        pausar_video = not pausar_video

video_path = 'Video.mp4'
cap = cv2.VideoCapture(video_path, cv2.CAP_MSMF)

#Comprueba que el video se abra correctamente
if not cap.isOpened():
    print('Error opening video stream or file')
else:
    print('Video is opened')

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_callback)

nuevo_alto = 425
nuevo_ancho = 700

#Limites para la mascara
upper_limit = np.array([])
lower_limit = np.array([])

def nothing(x):
    pass

#Crea controles deslizantes para ajustar la maskara
cv2.namedWindow("Trackbars")
cv2.createTrackbar("H min", "Trackbars", 7, 179, nothing)
cv2.createTrackbar("H max", "Trackbars", 170, 170, nothing)
cv2.createTrackbar("S min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V max", "Trackbars", 255, 255, nothing)

while True:
    if not pausar_video: #Mientras el video no está pausado
        ret, frame = cap.read()
        frame2 = np.copy(frame)
        if not ret:
            break
    if mostrar_pixel:
        pixel_color = frame[y, x]  #Obtener el valor del color en (x, y)
        frame2 = np.copy(frame)
        cv2.putText(frame2, f'Posición (x, y): ({x}, {y}) Color: {pixel_color}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame3 = cv2.resize(frame2, (nuevo_ancho, nuevo_alto))

    #Convertir bgr a hsv
    hsv = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    #Leer valores de las trackbars
    h_min = cv2.getTrackbarPos("H min", "Trackbars")
    h_max = cv2.getTrackbarPos("H max", "Trackbars")
    s_min = cv2.getTrackbarPos("S min", "Trackbars")
    s_max = cv2.getTrackbarPos("S max", "Trackbars")
    v_min = cv2.getTrackbarPos("V min", "Trackbars")
    v_max = cv2.getTrackbarPos("V max", "Trackbars")

    #Cear los rangos de colores
    bajo = np.array([h_min, s_min, v_min])
    alto = np.array([h_max, s_max, v_max])
    #Binarizar imagen
    mascara = cv2.inRange(hsv, bajo, alto)

    cv2.imshow('Video mascara', mascara)
    cv2.imshow('Video', hsv)

    key = cv2.waitKey(33) & 0xFF
    if key == 27:  # Presiona la tecla 'Esc' para salir
        break
cap.release()
cv2.destroyAllWindows()