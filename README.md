# Crucible-VM: Autonomous Self-Healing Data Pipelines with Hardware-Isolated LLM Execution

Una plataforma de ingeniería agéntica para la síntesis autónoma, validación estricta y ejecución en producción de transformaciones de datos (ETL) confinadas en microVMs de Firecracker con aislamiento por hardware (KVM).

## Métricas de Rendimiento
- **Latencia promedio por ciclo:** 1810.2 ms
- **Aislamiento:** 100% KVM Hardware Contained
- **Memoria por microVM:** 1024 MB (RAM efímera en tmpfs)

## 📊 Enterprise Stress Test Benchmark (50,000 Rows)

Evaluación rigurosa de rendimiento y contención de hardware ejecutada con datos sintéticos caóticos (*schema drift*, valores nulos aleatorios, formatos mixtos e inyecciones de código):

| Métrica | Resultado Medido | Contexto de Ingeniería |
| :--- | :--- | :--- |
| **Volumen de entrada** | 50,000 registros | 32,069 campos nulos/corruptos inyectados |
| **Tiempo de auto-curación** | **1.47 s** | Inferencia LLM + validación Pytest en microVM + ETL |
| **Throughput efectivo** | **33,956 filas/s** | Transformaciones vectorizadas sobre Pandas |
| **Huella RAM pico host** | **178.55 MB** | Delta de solo +39.19 MB en el sistema host |
| **Aislamiento de hardware** | **100% Contenido** | Cero impacto por inyecciones en el kernel host |

