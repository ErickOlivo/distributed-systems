from fastapi import FastAPI, Request
from jsonschema import validate, ValidationError
import time

app = FastAPI()

REQUEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "request_id": {"type": "string"},
        "client": {"type": "object", "properties": {"username": {"type": "string"}}},
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["request_id", "client", "timestamp"]
}

# 2. Esquema de Response
RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "task_id": {"type": "string"},
        "status": {"type": "string"},
        "message": {"type": "string"}
    },
    "required": ["task_id", "status", "message"]
}

@app.post("/actividad1")
async def procesar_actividad1(request: Request):
    start_total_time = time.time()
    payload = await request.json()
    
    # 3. Validar el Request 
    start_req_val = time.time()
    try:
        validate(instance=payload, schema=REQUEST_SCHEMA)
    except ValidationError as e:
        return {"error": f"Request Invalido: {e.message}"}
    req_val_overhead = (time.time() - start_req_val) * 1000

    # Simular tiempo de guardar en SQLite
    time.sleep(0.05)
    
    # Armar la respuesta
    response_data = {
        "task_id": payload.get("request_id"),
        "status": "Solicitado",
        "message": "Imagen recibida y validada contra JSON Schema"
    }
    
    # 4. Validar el Response antes de enviarlo 
    start_res_val = time.time()
    validate(instance=response_data, schema=RESPONSE_SCHEMA)
    res_val_overhead = (time.time() - start_res_val) * 1000
    
    total_overhead = req_val_overhead + res_val_overhead
    total_processing = (time.time() - start_total_time) * 1000
    
    # Añadimos métricas para que Jhony pueda calcular la latencia
    response_data["metrics"] = {
        "overhead_ms": total_overhead,
        "server_processing_time_ms": total_processing
    }
    
    return response_data
