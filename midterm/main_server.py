import zmq
import json

context = zmq.Context()
# Socket para escuchar a publishers y consumers
server = context.socket(zmq.REP)
server.bind("tcp://*:5555")

# Socket para sincronizar con el Replica Server
sync_socket = context.socket(zmq.REQ)
sync_socket.connect("tcp://localhost:5556")

registry = {}

print("Main Server running on port 5555...")

while True:
    msg = json.loads(server.recv().decode('utf-8'))
    
    if msg['type'] == 'register':
        service = msg['service']
        ip = msg['ip']
        port = msg['port']
        registry[service] = {'ip': ip, 'port': port}
        print(f"[MAIN] Registered {service} at {ip}:{port}")
        
        # Sincronizar con réplica
        sync_socket.send(json.dumps(msg).encode('utf-8'))
        sync_socket.recv() # Esperar ACK de la réplica

        server.send(json.dumps({"status": "ok"}).encode('utf-8'))
        
    elif msg['type'] == 'lookup':
        service = msg['service']
        print(f"[MAIN] Lookup request for {service}")
        if service in registry:
            server.send(json.dumps({"status": "ok", "data": registry[service]}).encode('utf-8'))
        else:
            server.send(json.dumps({"status": "error", "message": "Service not found"}).encode('utf-8'))
