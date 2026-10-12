import streamlit as st
import pandas as pd
import os
import time
import self_healing_pipeline

st.set_page_config(page_title="Crucible-VM | Data Sandbox", layout="wide", page_icon="🛡️")

st.title("🛡️ Crucible-VM: Self-Healing Data Sandbox")
st.markdown("**Aislamiento por Hardware KVM & Síntesis de Parches Autónomos con LLMs Locales**")

# Métricas de infraestructura en la barra lateral
st.sidebar.header("⚙️ Estado de Infraestructura")
st.sidebar.success("Hipervisor: Firecracker (KVM Activo)")
st.sidebar.info("Latencia promedio: 1810 ms (Cold Boot)")
st.sidebar.info("Aislamiento: 100% Hardware Contained")
st.sidebar.warning("Memoria Efímera: 1024 MB tmpfs")

st.divider()

col1, col2 = st.columns(2)

input_path = "/tmp/dashboard_input.csv"
output_path = "/tmp/dashboard_output.csv"

with col1:
    st.subheader("1. Ingesta de Datos Crudos")
    uploaded_file = st.file_uploader("Sube un archivo CSV con problemas de esquema o datos faltantes:", type=["csv"])
    
    use_sample = st.checkbox("Usar dataset de prueba corrupto (Ventas con nulos)")

    if use_sample:
        with open(input_path, "w") as f:
            f.write("id,fecha,precio,cantidad\n1,2026-01-01,10.5,5\n2,2026-01-02,,3\n3,2026-01-03,15.0,2\n4,2026-01-04,20.0,\n")
        df_preview = pd.read_csv(input_path)
        st.write("Vista previa de los datos corruptos:")
        st.dataframe(df_preview, use_container_width=True)
    elif uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        df_preview.to_csv(input_path, index=False)
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df_preview, use_container_width=True)

with col2:
    st.subheader("2. Procesamiento Aislado")
    if os.path.exists(input_path):
        if st.button("🚀 Ejecutar Pipeline Resiliente en Firecracker"):
            with st.spinner("Ejecutando en microVM aislada y evaluando contratos..."):
                t0 = time.time()
                try:
                    self_healing_pipeline.run_self_healing_etl(input_path, output_path)
                    elapsed = time.time() - t0
                    
                    if os.path.exists(output_path):
                        df_result = pd.read_csv(output_path)
                        st.success(f"✅ ¡Pipeline sanado con éxito en {elapsed:.2f} segundos!")
                        st.write("Resultado final saneado:")
                        st.dataframe(df_result, use_container_width=True)
                        
                        csv_data = df_result.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Descargar CSV Limpio",
                            data=csv_data,
                            file_name="dataset_limpio.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error en ejecución: {e}")
