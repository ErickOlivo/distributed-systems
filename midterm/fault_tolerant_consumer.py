import zmq
import json
import sys

if len(sys.argv) != 2:
    print("Usage: python fault_tolerant_consumer.py <SERVICE_NAME>")
    sys.exit(1)

service_name = sys.argv[1]
context = zmq.Context()

# 1. Preguntar al Main Server por la ubicación
req_socket = context.socket(zmq.REQ)
req_socket.connect("tcp://localhost:5555")

lookup_msg = {"type": "lookup", "service": service_name}
req_socket.send(json.dumps(lookup_msg).encode('utf-8'))

# Configurar Poller para manejar el Timeout (Tolerancia a fallos)
poller = zmq.Poller()
poller.register(req_socket, zmq.POLLIN)

# Esperar 3000 ms (3 segundos) por una respuesta
socks = dict(poller.poll(3000))

if socks.get(req_socket) == zmq.POLLIN:
    reply = json.loads(req_socket.recv().decode('utf-8'))
    print("Main Server responded successfully.")
else:
    print("Warning: Main Server timeout! Switching to Replica Server...")
    req_socket.close() # Cerrar el socket atascado
    
    # Conectar a la réplica
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://localhost:5556")
    req_socket.send(json.dumps(lookup_msg).encode('utf-8'))
    reply = json.loads(req_socket.recv().decode('utf-8'))

# 2. Conectarse al Publisher si se encontró el servicio
if reply['status'] == 'ok':
    pub_ip = reply['data']['ip']
    pub_port = reply['data']['port']
    print(f"Service '{service_name}' discovered at {pub_ip}:{pub_port}")
    
    # Lógica original de suscripción
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(f"tcp://{pub_ip}:{pub_port}")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, service_name)
    
    print(f"Listening for {service_name} messages...\n")
    for i in range(5):
        msg = sub_socket.recv().decode("utf-8")
        print(f"Received: {msg}")
else:
    print("Error: Service not available in the registry.")
