import cv2
import numpy as np

video_path = 'VideoRecortado.mp4'
cap = cv2.VideoCapture(video_path, cv2.CAP_MSMF)

if not cap.isOpened():
    print('Error opening video stream or file')
else:
    print('Video is opened')

# Dimensiones video
nuevo_ancho = 700
nuevo_alto = 425

# Arreglo para guardar los centroides
centroides = []

tiempo_inicio = 0
tiempo_fin = 0.635

fps = cap.get(cv2.CAP_PROP_FPS)
frame_inicio = int(tiempo_inicio * fps)
frame_fin = int(tiempo_fin * fps)

frame_num = 0

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([7, 0, 0])
    upper = np.array([170, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    # Operación morfológica de closing
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Mascara', mask)
    #cv2.imshow('HSV', hsv)

    if frame_inicio <= frame_num <= frame_fin:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                tiempo_segundos = frame_num / fps

                centroides.append((tiempo_segundos, cx, cy))

                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        #cv2.imshow("Centroides", frame)

    frame_num += 1

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Guardar en TXT
with open("centroides.txt", "w") as f:
    f.write("tiempo_segundos,cx,cy\n")
    for t, cx, cy in centroides:
        f.write(f"{t:.2f},{cx},{cy}\n")

