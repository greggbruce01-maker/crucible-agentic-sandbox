import os
import re
import pandas as pd
from openai import OpenAI
import skill_registry
import evaluator
import orchestrator

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_NAME = "qwen2.5-coder:7b"

def validate_data_contract(df: pd.DataFrame, initial_row_count: int) -> tuple[bool, str]:
    if df is None or df.empty:
        return False, "FALLO CRÍTICO: DataFrame vacío (0 registros retenidos)."
    if df.isnull().values.any():
        null_cols = df.columns[df.isnull().any()].tolist()
        return False, f"El DataFrame contiene valores nulos en: {null_cols}"
    if len(df) > initial_row_count:
        return False, "El DataFrame contiene más filas que el original."
    return True, f"Dataset válido: {len(df)} filas preservadas sin nulos."

def ensure_imports(code: str) -> str:
    imports = []
    if "import pandas as pd" not in code:
        imports.append("import pandas as pd")
    if "import numpy as np" not in code:
        imports.append("import numpy as np")
    return "\n".join(imports) + "\n\n" + code if imports else code

def synthesize_and_validate_new_skill(columns_info: list) -> str:
    print(f"\n[🔧 Auto-Healing]: Sintetizando herramienta a medida para {columns_info}...")
    
    test_harness = (
        "import pandas as pd\n"
        "from candidate import clean_dataset_strict\n"
        "def test_strict():\n"
        "    df = pd.DataFrame({\n"
        "        'id': [1, 2, 3],\n"
        "        'fecha': ['2026-01-01', '2026-01-02', '2026-01-03'],\n"
        "        'precio': [10.5, None, 15.0],\n"
        "        'cantidad': [5.0, 3.0, None]\n"
        "    })\n"
        "    res = clean_dataset_strict(df)\n"
        "    assert not res.empty, 'La función no puede vaciar el dataset'\n"
        "    assert len(res) == 1, f'Esperaba 1 fila válida, obtuvo {len(res)}'\n"
        "    assert res.iloc[0]['id'] == 1\n"
    )

    base_prompt = (
        f"Eres un ingeniero senior de datos. Escribe `def clean_dataset_strict(df):` en Python/Pandas.\n"
        f"REGLAS CRÍTICAS:\n"
        f"1. Incluye `import pandas as pd` al inicio.\n"
        f"2. Columnas presentes: {columns_info}.\n"
        f"3. Si existe 'fecha', usa: `df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')`\n"
        f"4. Columnas numéricas ('precio', 'cantidad', 'id'): usa `pd.to_numeric(df[col], errors='coerce')`\n"
        f"5. Elimina filas nulas: `df = df.dropna().reset_index(drop=True)` y devuelve `df.copy()`.\n"
        f"Devuelve ÚNICAMENTE el bloque dentro de ```python ... ```."
    )

    messages = [{"role": "user", "content": base_prompt}]

    for attempt in range(1, 4):
        print(f"  ├─ [Intento {attempt}/3] Generando parche con LLM...", end="", flush=True)
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0
        )
        raw_code = res.choices[0].message.content
        match = re.search(r"```python(.*?)```", raw_code, re.DOTALL)
        code = match.group(1).strip() if match else raw_code.strip()
        code = ensure_imports(code)
        print(" OK")

        print("  │  └─ Validando en MicroVM aislada...", end="", flush=True)
        eval_res = evaluator.run_agent_test(code, test_harness)
        
        if eval_res["success"]:
            print(" [Aprobado]")
            skill_path = os.path.join(skill_registry.SKILLS_DIR, "skill_strict_cleaner.py")
            with open(skill_path, "w") as f:
                f.write(code)
            print(f"  └─ ✅ ¡Nueva habilidad verificada y guardada en {os.path.basename(skill_path)}!")
            return code
        else:
            print(f" [Falló: {eval_res['stderr'].splitlines()[-1] if eval_res['stderr'] else 'Error'}]")
            messages.append({"role": "assistant", "content": f"```python\n{code}\n```"})
            messages.append({"role": "user", "content": f"Tu código falló en Pytest:\n{eval_res['stderr'][-600:]}\nCorrige la función asegurando imports y tipos."})

    raise RuntimeError("No se pudo sintetizar un parche funcional tras 3 intentos.")

def run_self_healing_etl(input_csv: str, output_csv: str):
    print("================================================================")
    print("🚀 INICIANDO PIPELINE DE DATOS AUTÓNOMO Y RESILIENTE")
    print("================================================================\n")
    
    df_raw = pd.read_csv(input_csv)
    initial_rows = len(df_raw)
    print(f"[1] Dataset crudo detectado ({initial_rows} registros):")
    print(df_raw)
    print("\n----------------------------------------------------------------")

    # 1. Probar herramientas del catálogo
    success = orchestrator.run_agentic_pipeline(
        user_prompt="Limpia completamente este dataset eliminando cualquier fila con datos faltantes",
        input_csv_path=input_csv,
        output_csv_path=output_csv
    )

    needs_repair = False
    fail_reason = ""

    if not success or not os.path.exists(output_csv):
        needs_repair = True
        fail_reason = "Herramienta falló en ejecución dentro de la MicroVM"
    else:
        df_result = pd.read_csv(output_csv)
        is_valid, report = validate_data_contract(df_result, initial_rows)
        if not is_valid:
            needs_repair = True
            fail_reason = report

    # 2. Desencadenar auto-reparación ante anomalías
    if needs_repair:
        print(f"\n[⚠️ Alerta de Calidad]: {fail_reason}")
        print("[!] Activando síntesis de herramienta en hardware aislado...")

        cols = df_raw.columns.tolist()
        new_skill = synthesize_and_validate_new_skill(columns_info=cols)

        print("\n[🚀 Despachando Parche]: Ejecutando herramienta verificada en Firecracker...")
        harness = (
            "import pandas as pd\n"
            "import candidate\n"
            "def test_run():\n"
            "    df = pd.read_csv('input.csv')\n"
            "    out = candidate.clean_dataset_strict(df)\n"
            "    assert not out.empty, 'El resultado no puede ser vacío'\n"
            "    print('\\n=== CSV_PAYLOAD_START ===')\n"
            "    print(out.to_csv(index=False).strip())\n"
            "    print('=== CSV_PAYLOAD_END ===\\n')\n"
        )

        res = evaluator.run_agent_test(
            solution_code=new_skill,
            test_suite=harness,
            data_files={"input.csv": input_csv},
            output_file=output_csv
        )

        if not res["success"] or not os.path.exists(output_csv):
            print(f"[Error Fatal]: {res['stderr']}")
            return

    print("\n=======================================================")
    print("🎉 PIPELINE FINALIZADO Y TOTALMENTE SANADO")
    print("=======================================================")
    final_df = pd.read_csv(output_csv)
    print(final_df)

if __name__ == "__main__":
    raw_path = "sample_data/raw_ventas.csv"
    clean_path = "sample_data/clean_ventas_repaired.csv"
    run_self_healing_etl(raw_path, clean_path)
