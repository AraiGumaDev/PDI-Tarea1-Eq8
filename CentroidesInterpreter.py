import matplotlib.pyplot as plt

# Leer el archivo
tiempos = []
xs = []
ys = []

with open("centroides.txt", "r") as f:
    next(f)  # saltar cabecera
    for line in f:
        t, cx, cy = line.strip().split(",")
        tiempos.append(float(t))
        xs.append(int(cx))
        ys.append(int(cy))

# Graficar trayectoria XY
plt.figure(figsize=(8, 6))
plt.scatter(xs, ys, c=tiempos, cmap="viridis", s=40, label="Centroides")
plt.colorbar(label="Tiempo (s)")
plt.gca().invert_yaxis()  # invertir eje Y para que coincida con imagen
plt.xlabel("X (px)")
plt.ylabel("Y (px)")
plt.title("Trayectoria del centro de la pelota")
plt.legend()
plt.show()
