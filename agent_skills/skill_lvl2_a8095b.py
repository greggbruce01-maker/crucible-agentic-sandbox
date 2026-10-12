import pandas as pd

def limpiar_datos(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes en 'precio' y 'cantidad'
    df = df.dropna(subset=['precio', 'cantidad']).reset_index(drop=True)
    
    # Convertir 'precio' y 'cantidad' a tipos numéricos
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    
    # Normalizar los nombres de los productos (en este caso, no hay errores evidentes)
    
    return df