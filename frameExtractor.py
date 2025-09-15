import cv2
import os

video_path = 'M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\VideoRecortado.mp4'
output_folder = 'M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\frames_extraidos'

#Crea la carpeta de salida
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)

#Verifica si el video se abrio
if not cap.isOpened():
    print(f"Error: No se pudo abrir el archivo de video en {video_path}")
else:
    frame_id = 0
    while True:
        #Lee el siguiente fotograma del video
        ret, frame = cap.read()

        #Si ret es False, significa que no hay más fotogramas
        if not ret:
            break

        #Guarda el fotograma como un archivo de imagen
        frame_filename = os.path.join(output_folder, f"frame_{frame_id:04d}.png")
        cv2.imwrite(frame_filename, frame)
        print(f"Fotograma guardado: {frame_filename}")

        frame_id += 1

    #Libera el objeto de captura de video
    cap.release()
    print("Proceso de extracción de fotogramas completado.")
