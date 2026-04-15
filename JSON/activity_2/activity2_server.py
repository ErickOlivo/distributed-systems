from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.post("/actividad2")
async def procesar_actividad2(request: Request):
    start_total_time = time.time()
    
    # 1. Parseo Schema-less (Simulando lectura rápida desde Redis)
    start_parse = time.time()
    
    # await request.json() decodifica el JSON sin validarlo contra un esquema estricto
    payload = await request.json() 
    
    parse_overhead = (time.time() - start_parse) * 1000

    # 2. Simular lógica del Router Worker (Extraer datos y enrutar)
    cultivo = payload.get("payload", {}).get("detected_crop", "Unknown")
    
    # Simulamos el tiempo de clasificación de la IA (ResNet18 ligera)
    time.sleep(0.05)
    
    # Armar la respuesta (También schema-less)
    response_data = {
        "task_id": payload.get("task_id"),
        "status": "Enrutado",
        "action": f"Mensaje procesado. Cultivo {cultivo} simulado.",
        "metrics": {
            "overhead_ms": parse_overhead,
            "server_processing_time_ms": (time.time() - start_total_time) * 1000
        }
    }
    
    return response_data
