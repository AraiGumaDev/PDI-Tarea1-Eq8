import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#Carga de archivos txt para crear los plots
centroides_file = "centroides.txt"              # archivo en px (tiempo_segundos,cx,cy)
params_file = "parametros_movimiento.txt"       # archivo en m (tiempo,x[m],y[m],...)
save_figs = True                                #Guarda PNGs

out_dir = "plots"                               #Guarda los plots en la carpeta plots
frame_height_px = 425                           # alto en px

os.makedirs(out_dir, exist_ok=True)

#---------- 1) Leer centroides en píxeles ----------
df_px = pd.read_csv(centroides_file)

if set(["tiempo_segundos", "cx", "cy"]).issubset(df_px.columns):
    t_px = df_px["tiempo_segundos"].values.astype(float)
    x_px = df_px["cx"].values.astype(float)
    y_px = df_px["cy"].values.astype(float)
else:
    t_px = df_px.iloc[:, 0].values.astype(float)
    x_px = df_px.iloc[:, 1].values.astype(float)
    y_px = df_px.iloc[:, 2].values.astype(float)

print(f"[INFO] {len(t_px)} puntos leídos desde {centroides_file} (píxeles).")

#---------- 2) Leer parámetros en metros ----------
df = pd.read_csv(params_file)

# Encuentra las columnas apropiadas
cols = [c.lower() for c in df.columns]
#Detectar columnas:
try:
    tcol = df.columns[[("tiempo" in c.lower()) for c in df.columns].index(True)]
except ValueError:
    tcol = df.columns[0]
try:
    xcol = df.columns[[("x[" in c.lower() or c.lower().startswith("x")) for c in df.columns].index(True)]
except ValueError:
    xcol = df.columns[1]
try:
    ycol = df.columns[[("y[" in c.lower() or c.lower().startswith("y")) for c in df.columns].index(True)]
except ValueError:
    ycol = df.columns[2]

#Mantener solo las columnas escenciales
df_phys = df[[tcol, xcol, ycol]].dropna().copy()
df_phys.columns = ["t", "x_m", "y_m"]  #Renombrado para trabajar cómodo

#Transformar a numpy
t = df_phys["t"].values.astype(float)
x_m = df_phys["x_m"].values.astype(float)
y_m = df_phys["y_m"].values.astype(float)

n = len(t)
print(f"[INFO] {n} puntos leídos desde {params_file} (metros).")

if n < 2:
    raise SystemExit("[ERROR] No hay suficientes puntos (menos de 2) en parametros_movimiento.txt para calcular velocidades.")

#Cambio de direccion del eje x, ya que la pelota va de derecha izquierda
#X crece cuando la pelota se desplaza de derecha a izquierda
x0_m = x_m[0]
x_m = x0_m - x_m

x0_px = x_px[0]
x_px_rel = x0_px - x_px

#---------- 3) limpiar dt==0 si existen ----------
dt = np.diff(t)
if np.any(dt == 0):
    print("[WARN] Se detectaron dt==0; eliminando filas con tiempos duplicados para evitar divisiones por cero.")
    # eliminar filas con tiempos duplicados
    _, idx = np.unique(t, return_index=True)
    df_phys = df_phys.iloc[np.sort(idx)].reset_index(drop=True)
    # rellenar t, x_m, y_m
    t = df_phys["t"].values.astype(float)
    x_m = df_phys["x_m"].values.astype(float)
    y_m = df_phys["y_m"].values.astype(float)
    #Se vuelve a aplicar la corrección a X
    x0_m = x_m[0]
    x_m = x0_m - x_m
    n = len(t)
    if n < 2:
        raise SystemExit("[ERROR] Tras eliminar duplicados no hay suficientes puntos.")
    dt = np.diff(t)

#---------- 4)Calcular velocidades y aceleraciones ----------
#Velocidades (length n-1), tiempos asociados times_v = t[1:]
vx = np.diff(x_m) / dt
vy = np.diff(y_m) / dt
v = np.sqrt(vx**2 + vy**2)
times_v = t[1:]

#Aceleraciones (length n-2), times_a = t[2:]
if len(vx) >= 2:
    dt2 = t[2:] - t[1:-1]  # length n-2
    ax = np.diff(vx) / dt2
    ay = np.diff(vy) / dt2
    a = np.sqrt(ax**2 + ay**2)
    times_a = t[2:]
else:
    ax = np.array([])
    ay = np.array([])
    a = np.array([])
    times_a = np.array([])

#Ángulo del vector velocidad (en grados) asociado a times_v
theta = np.degrees(np.arctan2(vy, vx))

# ---------- 5) Informationen y checks ----------
print(f"[INFO] puntos (m): {n}, puntos velocidad: {len(vx)}, puntos aceleracion: {len(ax)}")
if len(vx) != len(times_v):
    print("[WARN] Desalineamiento inesperado entre tiempos de velocidad y vx; se recortarán al mínimo al graficar.")

#Recortar para igualar longitudes
min_v_len = min(len(times_v), len(vx))
times_v = times_v[:min_v_len]
vx = vx[:min_v_len]
vy = vy[:min_v_len]
v = v[:min_v_len]
theta = theta[:min_v_len]

min_a_len = min(len(times_a), len(ax))
times_a = times_a[:min_a_len]
ax = ax[:min_a_len]
ay = ay[:min_a_len]
a = a[:min_a_len]

#---------- 6) Graficas ----------
#6.1 Trayectoria en pixeles (colormap por tiempo)
plt.figure(figsize=(8,6))
sc = plt.scatter(x_px_rel, y_px, c=t_px, cmap="viridis", s=40)
plt.colorbar(sc, label="Tiempo (s)")
plt.gca().invert_yaxis()
plt.xlabel("X (px) [derecha → izquierda]")
plt.ylabel("Y (px)")
plt.title("Trayectoria (píxeles) - referencia derecha → izquierda")
plt.grid(True)
if save_figs: plt.savefig(os.path.join(out_dir, "trayectoria_px.png"), dpi=200)
plt.show()

#6.2 Trayectoria en metros + ajuste cuadrático (parábola)
plt.figure(figsize=(8,6))
plt.plot(x_m, y_m, "o-", label="Trayectoria (m) - experimental (corr X)")
if n >= 3:
    #Ajustar parabola y = ax^2 + bx + c
    coeffs = np.polyfit(x_m, y_m, 2)
    xfit = np.linspace(np.min(x_m), np.max(x_m), 300)
    yfit = np.polyval(coeffs, xfit)
    plt.plot(xfit, yfit, "--", label=f"Ajuste cuadrático: y={coeffs[0]:.3e}x² + {coeffs[1]:.3e}x + {coeffs[2]:.3e}")
    #Error RMS
    y_pred = np.polyval(coeffs, x_m)
    rms = np.sqrt(np.mean((y_pred - y_m)**2))
    plt.text(0.02, 0.02, f"RMS ajuste = {rms:.4e} m", transform=plt.gca().transAxes)
plt.xlabel("X [m] [derecha → izquierda]")
plt.ylabel("Y [m]")
plt.title("Trayectoria en metros (experimental) con ajuste cuadrático")
plt.legend()
plt.grid(True)
if save_figs: plt.savefig(os.path.join(out_dir, "trayectoria_m_ajuste.png"), dpi=200)
plt.show()

#6.3 Velocidades vs tiempo (times_v)
if len(times_v) > 0:
    plt.figure(figsize=(10,6))
    plt.plot(times_v, vx, label="Vx [m/s] (derecha→izquierda positivo)")
    plt.plot(times_v, vy, label="Vy [m/s]")
    plt.plot(times_v, v, label="|V| [m/s]")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad [m/s]")
    plt.title("Velocidades en función del tiempo")
    plt.legend()
    plt.grid(True)
    if save_figs: plt.savefig(os.path.join(out_dir, "velocidades.png"), dpi=200)
    plt.show()
else:
    print("[WARN] No hay suficientes puntos para graficar velocidades.")

#6.4 Aceleraciones vs tiempo (times_a)
if len(times_a) > 0:
    plt.figure(figsize=(10,6))
    plt.plot(times_a, ax, label="Ax [m/s²] (derecha→izquierda positivo)")
    plt.plot(times_a, ay, label="Ay [m/s²]")
    plt.plot(times_a, a, label="|A| [m/s²]")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Aceleración [m/s²]")
    plt.title("Aceleraciones en función del tiempo")
    plt.legend()
    plt.grid(True)
    if save_figs: plt.savefig(os.path.join(out_dir, "aceleraciones.png"), dpi=200)
    plt.show()
else:
    print("[WARN] No hay suficientes puntos para graficar aceleraciones.")

#6.5 Ángulo del vector velocidad vs tiempo (times_v)
if len(times_v) > 0:
    plt.figure(figsize=(8,6))
    plt.plot(times_v, theta, "r-", label="Ángulo (°)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Ángulo [°]")
    plt.title("Ángulo del vector velocidad (dirección del movimiento)")
    plt.legend()
    plt.grid(True)
    if save_figs: plt.savefig(os.path.join(out_dir, "angulo.png"), dpi=200)
    plt.show()

#---------- 7) Guardar resultados resumidos  ----------
summary_file = "resumen_movimiento.csv"
df_out = pd.DataFrame({
    "t": t,
    "x_m": x_m,
    "y_m": y_m
})
#Añadir columnas de velocidad y aceleración alineadas (con NaN donde no existan)
df_out["vx"] = np.concatenate(([np.nan], vx)) if len(vx)>0 else np.nan
df_out["vy"] = np.concatenate(([np.nan], vy)) if len(vy)>0 else np.nan
df_out["v"]  = np.concatenate(([np.nan], v)) if len(v)>0 else np.nan
if len(ax)>0:
    df_out["ax"] = np.concatenate(([np.nan, np.nan], ax))
    df_out["ay"] = np.concatenate(([np.nan, np.nan], ay))
    df_out["a"]  = np.concatenate(([np.nan, np.nan], a))
else:
    df_out["ax"] = np.nan
    df_out["ay"] = np.nan
    df_out["a"] = np.nan
df_out["theta_deg"] = np.concatenate(([np.nan], theta)) if len(theta)>0 else np.nan
df_out.to_csv(summary_file, index=False)
print(f"[INFO] Resumen guardado en {summary_file}")
print("[DONE] Plots generados. Revisa la carpeta:", out_dir)