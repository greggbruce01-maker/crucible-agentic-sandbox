import pandas as pd

def limpiar_datos(df):
    # Crear una copia del DataFrame
    df = df.copy()
    
    # Convertir la columna 'valor' a tipo numérico
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    
    # Eliminar filas con valores nulos en la columna 'categoria'
    df = df.dropna(subset=['categoria'], how='any')
    
    # Eliminar filas con valores atípicos en la columna 'valor' (por ejemplo, valores mayores a 100)
    df = df[df['valor'] <= 100]
    
    # Resetear el índice del DataFrame
    df.reset_index(drop=True, inplace=True)
    
    return df