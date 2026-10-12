import pandas as pd

def limpiar_datos(df):
    df = df.copy()
    
    # Eliminar duplicados
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Manejar valores faltantes
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    
    return df