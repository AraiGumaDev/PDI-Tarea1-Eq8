import cv2
import os

cap = cv2.VideoCapture('M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\VideoRecortado.mp4')
output_folder = 'M:\\Users\\mahyro\\Documents\\Universidad\\2025-2\\Procesamiento Digital de Imagenes\\Tarea1\\VideoParaTrabajo1\\frames_extraidos'

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)

if fps > 0:  # Avoid division by zero
    duration_seconds = frame_count / fps
else:
    duration_seconds = 0
    print("Warning: FPS is zero, duration cannot be calculated.")

cap.release()

print(f"Video duration: {duration_seconds:.2f} seconds")