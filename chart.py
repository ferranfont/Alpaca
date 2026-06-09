# archivo: grafico.py

import matplotlib.pyplot as plt
import os

def graficar_precio(df, titulo="Gráfico de precios", columna="close", nombre_archivo=None):
    if df.empty or columna not in df.columns:
        print("❌ DataFrame vacío o columna no encontrada.")
        return
    
    os.makedirs("charts", exist_ok=True)    

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[columna], label=titulo, linewidth=2)
    plt.title(titulo)
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(axis="y")  # Solo líneas horizontales (eje Y)
    plt.legend()
    plt.tight_layout()

    # Nombre de archivo: usa el indicado o, si no, lo deriva del título
    if nombre_archivo:
        nombre = nombre_archivo
    else:
        nombre = "".join(c if c.isalnum() else "_" for c in titulo)
    ruta = f"charts/{nombre}.png"
    plt.savefig(ruta, bbox_inches='tight')
    print(f"📁 Gráfico guardado como: {ruta}")
    plt.show()


    
    

