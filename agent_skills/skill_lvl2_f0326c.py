import pandas as pd

def clean_data(df):
    df = df.copy()
    
    # Eliminar filas con valores faltantes en las columnas 'precio' y 'categoria'
    df = df.dropna(subset=['precio', 'categoria']).reset_index(drop=True)
    
    # Normalizar los datos en la columna 'precio' convirtiéndola a tipo numérico
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    return df