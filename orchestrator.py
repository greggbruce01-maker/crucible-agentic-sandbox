import json
import os
import shutil
import pandas as pd
from openai import OpenAI
import skill_registry
import evaluator

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_NAME = "qwen2.5-coder:7b"

def run_agentic_pipeline(user_prompt: str, input_csv_path: str, output_csv_path: str) -> bool:
    print(f"\n=======================================================")
    print(f"📥 Solicitud: \"{user_prompt}\"")
    print(f"📁 Dataset de entrada: {input_csv_path}")
    print(f"=======================================================")

    available_tools = skill_registry.get_available_tools_schema()
    if not available_tools:
        print("[!] No se encontraron herramientas en agent_skills/.")
        return False

    tools_desc = "\n".join([
        f"- {t['function']['name']}: {t['function']['description']}"
        for t in available_tools
    ])

    prompt = (
        f"Eres un Agente Orquestador de Datos. El usuario solicita:\n"
        f"\"{user_prompt}\"\n\n"
        f"Herramientas disponibles:\n{tools_desc}\n\n"
        f"Responde ÚNICAMENTE en JSON con el formato:\n"
        f'{{"selected_tool": "<nombre_de_la_herramienta>", "reason": "<motivo>"}}'
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    content = response.choices[0].message.content.strip()
    try:
        if "{" in content and "}" in content:
            json_str = content[content.find("{"):content.rfind("}")+1]
            decision = json.loads(json_str)
        else:
            decision = {"selected_tool": available_tools[0]['function']['name'], "reason": "Default"}
    except Exception:
        decision = {"selected_tool": available_tools[0]['function']['name'], "reason": "Fallback"}

    tool_name = decision.get("selected_tool")
    print(f"[🤖 Decisión]: Seleccionada `{tool_name}`")
    print(f"[📋 Motivo]: {decision.get('reason')}")

    skill_code = ""
    for fpath in skill_registry.glob.glob(os.path.join(skill_registry.SKILLS_DIR, "*.py")):
        with open(fpath, "r") as f:
            code = f.read()
            if f"def {tool_name}" in code:
                skill_code = code
                break

    if not skill_code:
        print(f"[!] No se encontró el código de `{tool_name}`.")
        return False

    test_harness = (
        f"import pandas as pd\n"
        f"import candidate\n"
        f"def test_execution():\n"
        f"    fn = getattr(candidate, '{tool_name}')\n"
        f"    df = pd.read_csv('input.csv')\n"
        f"    res = fn(df)\n"
        f"    assert res is not None\n"
        f"    assert len(res) > 0\n"
        f"    res.to_csv('output.csv', index=False)\n"
    )

    print(f"[🔒 Aislamiento]: Despachando a MicroVM de Firecracker...")
    result = evaluator.run_agent_test(
        solution_code=skill_code,
        test_suite=test_harness,
        data_files={"input.csv": input_csv_path},
        output_file="output.csv"
    )

    if result["success"]:
        if os.path.exists("output.csv"):
            shutil.move("output.csv", output_csv_path)
            print(f"[✅ Éxito]: Pipeline ejecutado de forma segura.")
            return True
        return False
    else:
        print(f"[❌ Fallo en MicroVM]:\n{result['stderr']}")
        return False
