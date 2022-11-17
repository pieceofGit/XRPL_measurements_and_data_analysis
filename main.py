ports = ["33", "333", "3332"]
node = {"port": "444"}
the_ports = ports
the_ports.append(node["port"])
print(ports)

dict = {"john": "5"}
print(dict.get("steve", 5))
ports = ["3", "33"]
for port in ports:
    print("YES")
    ports = []
import asyncio

import websockets

import asyncio
import websocket

async def hello():
    uri = "wss://38.146.7.11"
    import ssl
    
    # ssl_context = ssl.SSLContext(ssl.)
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(uri)
    # import ssl
    # name = input("What's your name? ")
    import json
    
    ws.send(json.dumps({"command":"server_info"}))
    # print(f">>> {name}")
    greeting = ws.recv()
    print(f"<<< {greeting}")
    eee = json.loads(greeting)
    print(eee)

if __name__ == "__main__":
    
   asyncio.run(hello())

