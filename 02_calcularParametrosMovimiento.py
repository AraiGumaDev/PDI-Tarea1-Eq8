import cv2
import numpy as np
import pandas as pd

video_path = 'Video.mp4'
#Archivo de los centroides previamente calculados
centroides_path = "centroides.txt"

# Escala de conversión de px am
diametro_metros = 0.074
diametro_px = 67
escala = diametro_metros / diametro_px  # metros por pixel

# Dimensiones del video para mostrar
nuevo_ancho = 700
nuevo_alto = 425

# columnas: tiempo_segundos,cx,cy
data = pd.read_csv(centroides_path)

tiempo = data["tiempo_segundos"].values
x_px = data["cx"].values
y_px = data["cy"].values

# Convertir a metros
x = x_px * escala
y = y_px * escala

dt = np.diff(tiempo)

#Velocidades
vx = np.diff(x) / dt
vy = np.diff(y) / dt
v = np.sqrt(vx**2 + vy**2)

#Aceleraciones
ax = np.diff(vx) / dt[:-1]
ay = np.diff(vy) / dt[:-1]
a = np.sqrt(ax**2 + ay**2)

#angulo
theta = np.degrees(np.arctan2(vy, vx))

# Guardar en TXT parametros_moviento.txt
with open("parametros_movimiento.txt", "w") as f:
    f.write("tiempo,x[m],y[m],vx[m/s],vy[m/s],v[m/s],ax[m/s^2],ay[m/s^2],a[m/s^2],angulo[deg]\n")
    for i in range(len(tiempo)):
        if i == 0:
            f.write(f"{tiempo[i]:.3f},{x[i]:.4f},{y[i]:.4f},,,,\n")
        elif i == 1:
            f.write(f"{tiempo[i]:.3f},{x[i]:.4f},{y[i]:.4f},{vx[i-1]:.4f},{vy[i-1]:.4f},{v[i-1]:.4f},,,,{theta[i-1]:.2f}\n")
        else:
            f.write(f"{tiempo[i]:.3f},{x[i]:.4f},{y[i]:.4f},{vx[i-1]:.4f},{vy[i-1]:.4f},{v[i-1]:.4f},{ax[i-2]:.4f},{ay[i-2]:.4f},{a[i-2]:.4f},{theta[i-1]:.2f}\n")

# --------------------
#Anotaciones en el video
# --------------------
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_num = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
    tiempo_actual = frame_num / fps

    idx = (np.abs(tiempo - tiempo_actual)).argmin()

    if idx < len(x_px):
        cx, cy = int(x_px[idx]), int(y_px[idx])
        cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

        if 1 <= idx < len(v):
            #Pinta el valor de la velocidad en el video
            cv2.putText(frame, f"Vel: {v[idx-1]:.2f} m/s", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            # Pinta el valor del angulo en el video
            cv2.putText(frame, f"Ang: {theta[idx-1]:.1f} deg", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        if idx >= 2 and idx-2 < len(a):
            #Pinta el valor de la aceleración en el vido
            cv2.putText(frame, f"Acel: {a[idx-2]:.2f} m/s^2", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Analisis Movimiento", frame)
    frame_num += 1

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
