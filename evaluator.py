import os
import re
import time
import uuid
import shutil
import subprocess
import requests_unixsocket

FC_DIR = os.path.abspath("firecracker_env")
KERNEL_PATH = os.path.join(FC_DIR, "vmlinux")
ROOTFS_PATH = os.path.join(FC_DIR, "rootfs.ext4")
FC_BINARY = os.path.join(FC_DIR, "firecracker")

def run_agent_test(solution_code: str, test_suite: str, data_files: dict = None, output_file: str = None):
    run_id = uuid.uuid4().hex[:8]
    work_dir = os.path.abspath(f"/tmp/fc_run_{run_id}")
    payload_dir = os.path.join(work_dir, "payload")
    os.makedirs(payload_dir, exist_ok=True)
    
    scratch_img = os.path.join(work_dir, "scratch.ext4")
    socket_path = os.path.join(work_dir, "firecracker.sock")
    api_url = f"http+unix://{socket_path.replace('/', '%2F')}"

    # Limpiar archivo de salida previo en el host para evitar lecturas residuales
    if output_file and os.path.exists(output_file):
        os.remove(output_file)

    # Inyectar archivos de datos
    if data_files:
        for guest_rel_path, host_path in data_files.items():
            dest = os.path.join(payload_dir, guest_rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(host_path, dest)

    test_imports = re.findall(r"from candidate import\s+([a-zA-Z0-9_]+)", test_suite)
    alias_bridge = "\n\n# Auto-bridge de compatibilidad\nimport sys\n_mod = sys.modules[__name__]\n"
    alias_bridge += "_funcs = [v for k, v in list(_mod.__dict__.items()) if callable(v) and not k.startswith('_')]\n"
    alias_bridge += "if _funcs:\n"
    for target in set(test_imports + ["clean_data", "clean_sales_data", "clean_dataset_strict", "limpiar_ventas", "solution"]):
        alias_bridge += f"    if '{target}' not in _mod.__dict__:\n        _mod.__dict__['{target}'] = _funcs[-1]\n"

    with open(os.path.join(payload_dir, "candidate.py"), "w") as f:
        f.write(solution_code + alias_bridge)

    with open(os.path.join(payload_dir, "test_candidate.py"), "w") as f:
        f.write(f"import candidate\n{test_suite}")

    res_mkfs = subprocess.run(
        ["mke2fs", "-q", "-F", "-d", payload_dir, "-t", "ext4", scratch_img, "16M"],
        capture_output=True,
        text=True
    )
    if res_mkfs.returncode != 0:
        shutil.rmtree(work_dir, ignore_errors=True)
        return {"success": False, "stdout": "", "stderr": f"Error mke2fs: {res_mkfs.stderr}", "csv_data": None}

    fc_proc = subprocess.Popen(
        [FC_BINARY, "--api-sock", socket_path],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(0.08)

    session = requests_unixsocket.Session()

    try:
        session.put(f"{api_url}/boot-source", json={
            "kernel_image_path": KERNEL_PATH,
            "boot_args": "init=/init.sh console=ttyS0 reboot=k panic=1 pci=off quiet"
        }).raise_for_status()

        try:
            session.put(f"{api_url}/entropy", json={}).raise_for_status()
        except Exception:
            pass

        session.put(f"{api_url}/drives/rootfs", json={
            "drive_id": "rootfs",
            "path_on_host": ROOTFS_PATH,
            "is_root_device": True,
            "is_read_only": True
        }).raise_for_status()

        session.put(f"{api_url}/drives/scratch", json={
            "drive_id": "scratch",
            "path_on_host": scratch_img,
            "is_root_device": False,
            "is_read_only": False
        }).raise_for_status()

        session.put(f"{api_url}/machine-config", json={
            "vcpu_count": 1,
            "mem_size_mib": 1024
        }).raise_for_status()

        session.put(f"{api_url}/actions", json={"action_type": "InstanceStart"}).raise_for_status()

        stdout, _ = fc_proc.communicate(timeout=20)

        match_body = re.search(r"=== PYTEST_START ===(.*?)=== PYTEST_END ===", stdout, re.DOTALL)
        match_exit = re.search(r"PYTEST_EXIT:(\d+)", stdout)

        csv_content = None
        match_csv = re.search(r"=== CSV_PAYLOAD_START ===\s*\n(.*?)\s*=== CSV_PAYLOAD_END ===", stdout, re.DOTALL)
        if match_csv:
            csv_content = match_csv.group(1).strip()

        if match_exit and match_body:
            exit_code = int(match_exit.group(1))
            body = match_body.group(1).strip()
            
            if exit_code == 0 and output_file and csv_content:
                os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
                with open(output_file, "w") as f:
                    f.write(csv_content + "\n")

            return {
                "success": (exit_code == 0),
                "stdout": body if exit_code == 0 else "",
                "stderr": body if exit_code != 0 else "",
                "csv_data": csv_content
            }
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error capturando salida en VM:\n{stdout[-400:]}",
                "csv_data": None
            }

    except subprocess.TimeoutExpired as e:
        fc_proc.kill()
        raw = e.stdout or ""
        out_str = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        return {"success": False, "stdout": "", "stderr": f"Error: Timeout en microVM (>20s).\nSalida:\n{out_str[-400:]}", "csv_data": None}
    except Exception as e:
        if fc_proc.poll() is None:
            fc_proc.kill()
        return {"success": False, "stdout": "", "stderr": f"Error del hipervisor: {str(e)}", "csv_data": None}
    finally:
        if fc_proc.poll() is None:
            fc_proc.kill()
        shutil.rmtree(work_dir, ignore_errors=True)
