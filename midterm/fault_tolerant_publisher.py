import zmq
import time
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python fault_tolerant_publisher.py <SERVICE_NAME> <PORT>")
    sys.exit(1)

service_name = sys.argv[1]
pub_port = sys.argv[2]
pub_ip = "127.0.0.1"

context = zmq.Context()

# 1. Registrar el servicio en el Main Server
req_socket = context.socket(zmq.REQ)
req_socket.connect("tcp://localhost:5555")

reg_msg = {"type": "register", "service": service_name, "ip": pub_ip, "port": pub_port}
req_socket.send(json.dumps(reg_msg).encode('utf-8'))
reply = json.loads(req_socket.recv().decode('utf-8'))
print(f"Registration status: {reply['status']}")
req_socket.close()

# 2. Iniciar la publicación (Lógica original modificada)
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{pub_port}")

print(f"Publisher offering '{service_name}' on port {pub_port}...")

while True:
    time.sleep(2)
    # Formato: "TOPICO Mensaje"
    msg = f"{service_name} Data update at {time.asctime()}"
    pub_socket.send(msg.encode("utf-8"))
