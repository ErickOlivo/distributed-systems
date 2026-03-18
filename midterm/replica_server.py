import zmq
import json

context = zmq.Context()
server = context.socket(zmq.REP)
server.bind("tcp://*:5556")

registry = {}

print("Replica Server running on port 5556...")

while True:
    msg = json.loads(server.recv().decode('utf-8'))
    
    if msg['type'] == 'register':
        service = msg['service']
        ip = msg['ip']
        port = msg['port']
        registry[service] = {'ip': ip, 'port': port}
        print(f"[REPLICA] Synced {service} at {ip}:{port}")
        server.send(json.dumps({"status": "ok"}).encode('utf-8'))
        
    elif msg['type'] == 'lookup':
        service = msg['service']
        print(f"[REPLICA] Fallback lookup request for {service}")
        if service in registry:
            server.send(json.dumps({"status": "ok", "data": registry[service]}).encode('utf-8'))
        else:
            server.send(json.dumps({"status": "error", "message": "Service not found"}).encode('utf-8'))
