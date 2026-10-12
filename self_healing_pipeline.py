import os
import sys
import json
import time
import subprocess
import pandas as pd
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL_NAME = "qwen2.5-coder:7b"
FC_RUNNER = "./fc_run.sh"

def build_dynamic_test_harness(sample_df: pd.DataFrame, function_name: str = "clean_data"):
    columns = list(sample_df.columns)
    sample_records = sample_df.head(5).to_dict(orient="records")
    
    test_code = f'''import pytest
import pandas as pd
import numpy as np

NaN = float('nan')
null = None
Infinity = float('inf')

from candidate import {function_name}

def test_dynamic_schema():
    raw_data = {json.dumps(sample_records, default=str)}
    df_in = pd.DataFrame(raw_data)
    
    df_out = {function_name}(df_in)
    
    assert isinstance(df_out, pd.DataFrame), "El retorno debe ser un DataFrame de Pandas"
    assert len(df_out.columns) == len(df_in.columns), "No se deben perder columnas del esquema"
    assert df_out.isna().sum().sum() == 0, "No deben quedar valores nulos tras la limpieza estricta"
'''
    with open("test_candidate.py", "w") as f:
        f.write(test_code)

def generate_patch_with_llm(columns, sample_rows, error_log=""):
    prompt = f"""Escribe una función de Python llamada `clean_data(df: pd.DataFrame) -> pd.DataFrame` usando Pandas.
Columnas del dataset: {columns}
Muestra de datos crudos:
{sample_rows}

Reglas estrictas de codificación:
1. La función DEBE llamarse `clean_data`.
2. Para columnas numéricas o monetarias ('amount', 'quantity', 'precio'):
   Usa estrictamente la función global pd.to_numeric envolviendo la serie limpia:
   df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^0-9.-]', '', regex=True), errors='coerce')
3. Para columnas de fecha/tiempo ('timestamp', 'fecha'):
   df[col] = pd.to_datetime(df[col], errors='coerce')
4. Elimina cualquier fila que contenga nulos resultantes usando: df = df.dropna()
5. Devuelve únicamente el código Python puro, sin bloques markdown (sin ```python ni ```).
"""
    if error_log:
        prompt += f"\nError previo en Pytest que debes solucionar:\n{error_log}\n"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    code = response.choices[0].message.content.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()

def run_isolated_pytest():
    if not os.path.exists(FC_RUNNER):
        res = subprocess.run(["pytest", "test_candidate.py"], capture_output=True, text=True)
        return res.returncode, res.stdout + res.stderr

    cmd = ["bash", FC_RUNNER, "pytest test_candidate.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout + res.stderr

def run_self_healing_etl(input_csv: str, output_csv: str):
    df_raw = pd.read_csv(input_csv)
    columns = list(df_raw.columns)
    print(f"\n[+] Dataset ingresado: {len(df_raw)} filas. Columnas: {columns}")
    
    build_dynamic_test_harness(df_raw, function_name="clean_data")
    
    max_retries = 3
    patch_success = False
    last_error = ""
    
    for attempt in range(1, max_retries + 1):
        print(f"[*] [Intento {attempt}/{max_retries}] Sintetizando parche adaptado al esquema...")
        code = generate_patch_with_llm(columns, df_raw.head(3).to_string(), error_log=last_error)
        
        with open("candidate.py", "w") as f:
            f.write("import pandas as pd\nimport numpy as np\n\n" + code + "\n")
            
        print("    Validando candidato en microVM aislada...")
        retcode, logs = run_isolated_pytest()
        
        if retcode == 0:
            print("    [✓] ¡Candidato APROBADO por Pytest dentro de la microVM!")
            patch_success = True
            break
        else:
            print(f"    [X] Falló validación en microVM (Exit code: {retcode}).")
            # Mostrar las líneas de error de Pytest directamente en pantalla
            error_lines = [l for l in logs.splitlines() if "FAILED" in l or "Error" in l or "assert" in l]
            for el in error_lines[-3:]:
                print(f"        -> {el}")
            last_error = "\n".join(logs.splitlines()[-10:])
            
    if not patch_success:
        raise RuntimeError("No se pudo sintetizar un parche válido tras 3 intentos.")
        
    print("[+] Ejecutando transformación aprobada sobre el dataset completo...")
    import importlib
    import candidate
    importlib.reload(candidate)
    
    df_clean = candidate.clean_data(df_raw)
    df_clean.to_csv(output_csv, index=False)
    print(f"[✓] Transformación finalizada: {len(df_clean)} filas guardadas en {output_csv}")
