# archivo: grafico.py

import matplotlib.pyplot as plt
import os

def graficar_precio(df, titulo="Gráfico de precios", columna="close"):
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
    plt.savefig('charts/AAPL_-_Precio_de_cierre.png', bbox_inches='tight')
    print(f"📁 Gráfico guardado como: charts/AAPL_-_Precio_de_cierre.png")
    plt.show()


    
    

