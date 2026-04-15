import requests
import json
import time

# IP de Erick apuntando al nuevo endpoint
URL_ERICK = "http://172.23.207.8:8001/actividad2"

# Datos a enviar (Internal Payload - Simulación de Redis)
internal_payload = {
    "task_id": "req-ui-001",
    "client_metadata": {"username": "jhony_p"},
    "timestamp": "2026-04-15T10:05:00Z",
    "payload": {
        "image_path": "/shared_data/img-123.jpg",
        "detected_crop": "Pending"
    },
    "state": {
        "current_status": "Queued"
    }
}

print("ACTIVIDAD 2: TRANSFERENCIA SCHEMA-LESS")

# 1. Medir bytes de envío
json_str = json.dumps(internal_payload)
bytes_sent = len(json_str.encode('utf-8'))

# 2. Medir tiempo total de ida y vuelta (RTT)
start_rtt = time.time()
response = requests.post(URL_ERICK, json=internal_payload)
total_rtt_ms = (time.time() - start_rtt) * 1000

# 3. Medir bytes de respuesta
bytes_received = len(response.text.encode('utf-8'))

data = response.json()

# 4. Extraer métricas y calcular latencia pura
if "metrics" in data:
    server_time = data["metrics"]["server_processing_time_ms"]
    overhead = data["metrics"]["overhead_ms"]
    network_latency = total_rtt_ms - server_time
    
    print("\n[RESULTADOS DE TRANSFERENCIA]")
    print(f"-> Datos enviados: {bytes_sent} bytes")
    print(f"-> Datos recibidos: {bytes_received} bytes")
    print(f"-> Latencia pura de red: {network_latency:.4f} ms")
    print(f"-> Overhead de parseo básico (Server): {overhead:.4f} ms")
    print("\n[RESPUESTA DEL SERVIDOR]")
    print(f"Estado: {data['status']} | Acción: {data['action']}")
else:
    print("Error:", data)
