import pandas as pd

def limpiar_ventas(df):
    df = df.copy()
    # Eliminar filas donde el valor de 'precio' sea NaN
    df = df.dropna(subset=['precio']).reset_index(drop=True)
    # Convertir el valor de 'precio' a tipo float, eliminando cualquier carácter no numérico
    df['precio'] = pd.to_numeric(df['precio'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    return df