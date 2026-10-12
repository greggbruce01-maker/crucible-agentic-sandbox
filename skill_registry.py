import ast
import glob
import os

SKILLS_DIR = os.path.abspath("agent_skills")

def parse_python_functions(filepath: str):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())
    
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            docstring = ast.get_docstring(node) or f"Transformación de datos implementada en {os.path.basename(filepath)}"
            params = [arg.arg for arg in node.args.args]
            functions.append({
                "name": node.name,
                "description": docstring,
                "parameters": params,
                "file_path": filepath
            })
    return functions

def get_available_tools_schema():
    tools = []
    skill_files = glob.glob(os.path.join(SKILLS_DIR, "*.py"))
    
    for fpath in skill_files:
        funcs = parse_python_functions(fpath)
        for fn in funcs:
            tools.append({
                "type": "function",
                "function": {
                    "name": fn["name"],
                    "description": fn["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input_path": {
                                "type": "string",
                                "description": "Ruta relativa o absoluta del dataset que se va a procesar."
                            }
                        },
                        "required": ["input_path"]
                    }
                }
            })
    return tools

if __name__ == "__main__":
    schemas = get_available_tools_schema()
    print(f"[+] Herramientas registradas dinámicamente: {len(schemas)}")
    for t in schemas:
        print(f"  - {t['function']['name']}: {t['function']['description'][:60]}...")
