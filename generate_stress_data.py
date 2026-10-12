import pandas as pd
import numpy as np
import random

NUM_ROWS = 50000

print(f"Generando dataset empresarial de prueba con {NUM_ROWS} registros corruptos...")

dates = [
    "2026-01-15", "15/01/2026", "Jan 15, 2026", "2026.01.15", 
    None, "INVALID_DATE", "1900-01-01"
]

prices = [
    "$1,250.50", "300.00", "€45.99", "-150.00", "FREE", 
    None, "NaN", "999999.99", "12.5"
]

quantities = [1, 2, 5, 10, -3, 0, None, "ten", 100]

customers = [
    "ACME Corp", "GlobalLogistics", "TechNova", 
    "'; DROP TABLE transactions; --",  # SQL Injection test
    "__import__('os').system('whoami')", # Code Injection test
    None
]

data = {
    "transaction_id": [f"TX-{i:06d}" for i in range(1, NUM_ROWS + 1)],
    "timestamp": [random.choice(dates) for _ in range(NUM_ROWS)],
    "amount": [random.choice(prices) for _ in range(NUM_ROWS)],
    "quantity": [random.choice(quantities) for _ in range(NUM_ROWS)],
    "customer": [random.choice(customers) for _ in range(NUM_ROWS)]
}

df = pd.DataFrame(data)
output_file = "stress_test_50k.csv"
df.to_csv(output_file, index=False)

print(f"Archivo '{output_file}' generado con éxito ({round(df.memory_usage().sum() / 1024**2, 2)} MB).")
