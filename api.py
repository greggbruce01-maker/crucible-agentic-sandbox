import os
import shutil
import uuid
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import self_healing_pipeline

app = FastAPI(
    title="Crucible-VM Isolated Data Engine",
    description="API empresarial para procesamiento y auto-curación de datos en microVMs Firecracker aisladas por hardware.",
    version="1.0.0"
)

TEMP_DIR = "/tmp/crucible_api_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "engine": "Firecracker KVM MicroVM",
        "isolation_level": "Hardware Contained"
    }

@app.post("/api/v1/clean-data")
async def clean_data_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Solo se admiten archivos .csv")

    job_id = uuid.uuid4().hex[:8]
    raw_path = os.path.join(TEMP_DIR, f"raw_{job_id}.csv")
    cleaned_path = os.path.join(TEMP_DIR, f"clean_{job_id}.csv")

    try:
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        df_initial = pd.read_csv(raw_path)
        initial_count = len(df_initial)

        self_healing_pipeline.run_self_healing_etl(
            input_csv=raw_path,
            output_csv=cleaned_path
        )

        if not os.path.exists(cleaned_path):
            raise HTTPException(status_code=500, detail="Fallo en la ejecución dentro de la microVM")

        df_cleaned = pd.read_csv(cleaned_path)
        final_count = len(df_cleaned)

        return JSONResponse(content={
            "job_id": job_id,
            "status": "SUCCESS",
            "initial_rows": initial_count,
            "final_rows": final_count,
            "rows_retained": final_count,
            "data": df_cleaned.to_dict(orient="records")
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(raw_path):
            os.remove(raw_path)
        if os.path.exists(cleaned_path):
            os.remove(cleaned_path)
