import requests
import json
import time

# IP de Erick
URL_ERICK = "http://172.23.207.8:8001/actividad1"

# Datos a enviar (Request)
payload = {
    "request_id": "req-ui-001",
    "client": {"username": "jhony_p"},
    "timestamp": "2026-04-15T10:00:00Z"
}

print("ACTIVIDAD 1: JSON SCHEMA ESTRICTO")

# 1. Medir bytes de envío [cite: 19]
json_str = json.dumps(payload)
bytes_sent = len(json_str.encode('utf-8'))

# 2. Medir tiempo total de ida y vuelta (RTT)
start_rtt = time.time()
response = requests.post(URL_ERICK, json=payload)
total_rtt_ms = (time.time() - start_rtt) * 1000

# 3. Medir bytes de respuesta [cite: 19]
bytes_received = len(response.text.encode('utf-8'))

data = response.json()

# 4. Extraer métricas y calcular latencia pura [cite: 19]
if "metrics" in data:
    server_time = data["metrics"]["server_processing_time_ms"]
    overhead = data["metrics"]["overhead_ms"]
    network_latency = total_rtt_ms - server_time
    
    print("\n[RESULTADOS DE TRANSFERENCIA]")
    print(f"-> Datos enviados: {bytes_sent} bytes")
    print(f"-> Datos recibidos: {bytes_received} bytes")
    print(f"-> Latencia pura de red: {network_latency:.4f} ms")
    print(f"-> Overhead de validación JSON Schema (Server): {overhead:.4f} ms")
    print("\n[RESPUESTA DEL BROKER]")
    print(f"Estado: {data['status']} | Mensaje: {data['message']}")
else:
    print("Error:", data)
