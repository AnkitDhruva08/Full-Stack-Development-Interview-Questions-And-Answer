WebSocket Questions & Detailed Answers
1. What is a WebSocket?
What:
A protocol providing full-duplex communication channels over a single, long-lived TCP connection between client and server.

Why:
For real-time, bidirectional communication between browser and server (e.g., chats, live feeds).

How:
After an initial HTTP handshake, the protocol upgrades to WebSocket, allowing low-latency, persistent connection.

Benefits:

Reduced overhead compared to HTTP polling.

Instant data push from server to client.

Efficient real-time applications.

If not used:
You'd rely on inefficient HTTP polling or long-polling, causing latency and overhead.

2. How does WebSocket differ from HTTP?
What:
HTTP is request-response; WebSocket is persistent, full-duplex.

Why:
HTTP is stateless and unidirectional; WebSocket enables ongoing two-way communication.

How:
WebSocket connection starts with HTTP handshake, then switches protocol.

Benefits:
Real-time, interactive apps like games, chat, live notifications.

If replaced with HTTP:
Increased latency, overhead, and limited interactivity.

3. What is the WebSocket handshake?
What:
Initial HTTP/1.1 request with Upgrade: websocket header from client to server.

Why:
To switch from HTTP protocol to WebSocket protocol.

How:
Server responds with status 101 Switching Protocols confirming upgrade.

Benefits:
Seamless transition from HTTP to WebSocket on same port (usually 80/443).

4. Explain the WebSocket message format
What:
Messages are sent as frames (text, binary, ping/pong, close).

Why:
Allows efficient, multiplexed communication.

How:
Frames have small headers + payload, enabling low overhead.

Benefits:
Supports text and binary data, control frames for connection health.

5. What are common use cases of WebSocket?
Real-time chat apps

Live sports/stock updates

Multiplayer games

Collaborative editing tools

IoT device communication

6. How to create a simple WebSocket server in Python? (using websockets library)
python
Copy
Edit
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
Explanation:
Server listens on localhost:8765, echoes back received messages.

7. How to connect to WebSocket from JavaScript client?
js
Copy
Edit
const socket = new WebSocket('ws://localhost:8765');

socket.onopen = () => {
  console.log('Connection opened');
  socket.send('Hello Server!');
};

socket.onmessage = (event) => {
  console.log('Message from server:', event.data);
};

socket.onclose = () => console.log('Connection closed');
socket.onerror = (error) => console.error('WebSocket error:', error);
8. What is the difference between ws:// and wss://?
What:
ws:// is unencrypted WebSocket, wss:// is secure (over TLS/SSL).

Why:
Secure communication is required to protect data privacy/integrity.

Benefits:
Protects against man-in-the-middle attacks.

If not used:
Data transmitted in plaintext, vulnerable to interception.

9. What is a WebSocket ping/pong frame?
What:
Control frames sent to check connection health.

Why:
To detect dead connections and keep the connection alive through proxies/firewalls.

How:
Server or client sends ping; the other replies with pong automatically.

10. How do you handle connection errors and reconnection?
What:
WebSocket can close unexpectedly due to network issues.

How:
Implement retry logic with exponential backoff on the client side.

Benefits:
Improves app resilience and user experience.

11. Can WebSocket be used across domains?
What:
Yes, but browsers enforce CORS-like security rules.

Why:
Prevent unauthorized connections.

How:
Server must allow cross-origin WebSocket connections via headers or authentication.

12. How to scale WebSocket servers?
Use Load Balancers that support sticky sessions or session affinity (to maintain connection to the same server).

Use Message Brokers like Kafka or Redis Pub/Sub to distribute messages among servers.

Consider WebSocket clusters behind proxies (NGINX, HAProxy).

13. What is the difference between WebSocket and HTTP/2 Server Push?
WebSocket supports full-duplex, persistent communication.

HTTP/2 Server Push is server-initiated push but unidirectional and not a persistent two-way channel.

14. How to close a WebSocket connection properly?
Client or server sends a Close Frame (opcode 0x8).

Peer acknowledges close and connection closes cleanly.

15. Example: Simple chat app backend in Python (using websockets)
python
Copy
Edit
import asyncio
import websockets

connected = set()

async def chat_handler(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

start_server = websockets.serve(chat_handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
16. What are limitations of WebSocket?
Not supported in very old browsers (mostly legacy issue now).

Requires WebSocket-compatible proxies/load balancers.

Long-lived connections consume resources on server.

17. What alternatives exist to WebSocket?
HTTP Polling: Client frequently polls server (high overhead).

Long Polling: Client sends request, server holds until data available (lower latency but still less efficient).

Server-Sent Events (SSE): One-way streaming from server to client only.

gRPC Web: For RPC over HTTP/2 with streaming.

18. Why use WebSocket instead of REST API?
REST is stateless, request-response only.

WebSocket is stateful, allows server push without client polling.

WebSocket reduces network overhead and latency for real-time apps.

19. How does WebSocket fit into microservices architecture?
Useful for real-time event communication between services or from backend to frontend.

Works with message brokers (Kafka, RabbitMQ) to scale events.

20. How to secure WebSocket connections?
Use TLS (wss://) for encryption.

Implement authentication during handshake (e.g., JWT tokens).

Validate input messages to prevent injection attacks.

Use rate limiting and firewall rules.

Summary Table for Quick Review
Question	Why Use It?	What If Not Used?	Example/Notes
WebSocket vs HTTP	Real-time, low latency comms	High latency, overhead	ws:// upgrade from HTTP
Ping/Pong	Keep connection alive	Stale/dead connections	Control frames
Consumer Groups (Kafka concept)	Scalability and load balancing	Bottleneck	Partition assignment
Scaling WebSocket	Support many clients	Resource exhaustion	Use Load balancer + Pub/Sub
Securing WebSocket	Protect data and user privacy	Vulnerable to MITM attacks	Use TLS and auth
Alternatives	Simpler or older systems	Lower efficiency	HTTP Polling, SSE




<!-- diffrence between kafka and web sockit -->

Difference between Kafka and WebSocket
Aspect	Kafka	WebSocket
What is it?	Distributed streaming platform/message broker.	Protocol for full-duplex, bidirectional communication over a single TCP connection.
Purpose	Durable, scalable event/message processing and streaming between distributed systems.	Real-time, interactive, low-latency communication between client (usually browser) and server.
Use case	Backend systems: logs aggregation, event sourcing, stream processing, microservices messaging.	Frontend-backend real-time updates like chat apps, notifications, live data feeds.
Communication type	Asynchronous, decoupled, many-to-many message passing.	Synchronous, persistent, full-duplex channel between two endpoints.
Message persistence	Messages stored durably on disk with configurable retention.	Messages are transient — exist only in connection memory, no built-in persistence.
Scalability	Highly scalable, partitioned topics allow parallel processing, replication for fault tolerance.	Limited scalability by server resources; usually one connection per client; horizontal scaling requires load balancers.
Protocol	Custom TCP-based protocol managed by Kafka brokers.	Standardized protocol that upgrades HTTP connection (ws:// or wss://).
Fault tolerance	Built-in replication and leader election for reliability.	No built-in fault tolerance; connection loss means message loss unless managed at application layer.
Latency	High throughput but with some latency due to disk writes and batching.	Very low latency, near real-time message delivery.
Typical clients	Backend services, data pipelines, stream processors.	Web browsers, mobile apps, real-time dashboards.
Message ordering	Guarantees ordering per partition.	Ordering guaranteed only by message arrival order over the connection.
Delivery semantics	Supports at-least-once, at-most-once, and exactly-once delivery modes.	Best effort delivery; application must handle message loss/retransmission.
Security	Supports TLS, SASL for authentication and encryption.	Uses TLS (wss://), but authentication must be implemented during handshake.
When to use?	When you need scalable, fault-tolerant, durable event streaming between distributed systems.	When you need instant, real-time, interactive communication between a client and server.
If not used / alternative	Without Kafka, large-scale event streaming is harder to manage, use traditional message queues or databases.	Without WebSocket, use HTTP polling/long-polling/SSE but with higher latency and overhead.

Summary:
Kafka = robust, scalable backend event streaming platform, excellent for handling huge volumes of data with durability and fault tolerance.

WebSocket = lightweight, real-time frontend-backend communication protocol, best for instant updates and interactive user experiences.

Example to visualize:
Scenario	Kafka	WebSocket
Real-time stock price updates	Use Kafka to ingest/process/store price data streams. Frontend subscribes via WebSocket to display live updates.	WebSocket pushes real-time updates from backend to client UI instantly.
Chat Application	Kafka used internally for message queuing, logging, and replay.	WebSocket used for direct real-time message exchange between clients and server.






[Stock Market Data Source]
           ↓ (raw data stream)
        [Kafka Broker Cluster]
           ↓ (processed & stored)
     [Backend Service / Processor]
           ↓ (push updates)
       [WebSocket Server]
           ↓ (push to)
       [Clients (Browsers)]
Kafka: Handles ingesting, storing, and processing high-volume stock price events reliably and scalably.

Backend Service: Consumes Kafka messages, processes business logic, then pushes updates to clients.

WebSocket Server: Maintains open connections to clients and pushes real-time data instantly.

Minimal Kafka Producer (Python)
python
Copy
Edit
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

stocks = ['AAPL', 'GOOG', 'TSLA']

while True:
    stock_update = {
        'symbol': random.choice(stocks),
        'price': round(random.uniform(100, 1500), 2)
    }
    producer.send('stock_prices', stock_update)
    print(f"Produced: {stock_update}")
    time.sleep(1)
Minimal Kafka Consumer + WebSocket Push (Python with websockets)
python
Copy
Edit
import asyncio
import json
import websockets
from kafka import KafkaConsumer

# Set of connected clients
connected = set()

async def websocket_handler(websocket, path):
    connected.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)

async def kafka_consumer():
    consumer = KafkaConsumer('stock_prices',
                             bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        data = json.dumps(message.value)
        # Broadcast to all connected clients
        if connected:
            await asyncio.wait([ws.send(data) for ws in connected])
        print(f"Sent to clients: {data}")

async def main():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    await kafka_consumer()

asyncio.run(main())
Minimal WebSocket Client (JavaScript)
js
Copy
Edit
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
  console.log('WebSocket connected');
};

ws.onmessage = (event) => {
  const stock = JSON.parse(event.data);
  console.log(`Stock Update: ${stock.symbol} - $${stock.price}`);
  // Update your UI here
};

ws.onclose = () => {
  console.log('WebSocket disconnected');
};
Why combine Kafka + WebSocket?
Kafka scales and stores huge event streams reliably.

WebSocket pushes those updates instantly to users with very low latency.

Together they provide a robust, real-time, scalable system.

What if you only use WebSocket (no Kafka)?
You lose durability & scalability.

Server may drop messages if overloaded.

No easy replay or audit of messages.

What if you only use Kafka (no WebSocket)?
You miss real-time push to client browsers.

Clients would have to poll backend for updates (higher latency and overhead).

If you want, I can also help you with:

Dockerizing this entire stack (Kafka + Zookeeper + Python app + WebSocket server)

More production-ready patterns (handling reconnect, error cases, auth)

Sample Docker Compose setup integrating Kafka + WebSocket service

Just ask!



<!-- Impltemnetation web sckoit  -->

# Complete WebSocket Guide with Python Code Examples

## WebSocket Fundamentals

### 1. What is WebSocket and Why is it Used?

**What is this?**
- Full-duplex communication protocol over a single TCP connection
- Persistent connection between client and server for real-time communication
- Upgrade from HTTP protocol enabling bidirectional data exchange

**Why do we use it?**
- Enable real-time communication without constant HTTP polling
- Reduce server load and network overhead
- Support interactive applications requiring instant updates
- Provide low-latency data exchange for time-sensitive applications

**How is it used?**
```python
# Client-side WebSocket (using websockets library)
import asyncio
import websockets
import json

async def client_example():
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        # Send message to server
        await websocket.send("Hello Server!")
        print("Message sent to server")
        
        # Receive message from server
        response = await websocket.recv()
        print(f"Response from server: {response}")
        
        # Send JSON data
        data = {"type": "message", "content": "Hello World"}
        await websocket.send(json.dumps(data))
        
        # Keep connection alive and listen
        async for message in websocket:
            print(f"Received: {message}")
            break

# Run client
# asyncio.run(client_example())
```

```python
# Server-side WebSocket (using websockets library)
import asyncio
import websockets
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients
connected_clients = set()

async def handle_client(websocket, path):
    """Handle individual client connections"""
    connected_clients.add(websocket)
    client_ip = websocket.remote_address[0]
    logger.info(f"Client {client_ip} connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            logger.info(f"Received from {client_ip}: {message}")
            
            # Echo message back
            await websocket.send(f"Echo: {message}")
            
            # Broadcast to all clients
            if connected_clients:
                await broadcast_message(f"Broadcast from {client_ip}: {message}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_ip} disconnected")
    except Exception as e:
        logger.error(f"Error handling client {client_ip}: {e}")
    finally:
        connected_clients.remove(websocket)

async def broadcast_message(message):
    """Broadcast message to all connected clients"""
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

# Start server
async def start_server():
    server = await websockets.serve(handle_client, "localhost", 8765)
    logger.info("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Run server
# asyncio.run(start_server())
```

**Benefits:**
- **Real-time Communication**: Instant bidirectional data exchange
- **Low Latency**: No HTTP request/response overhead
- **Reduced Server Load**: Single persistent connection vs multiple HTTP requests
- **Efficiency**: Lower bandwidth usage compared to polling
- **Simplicity**: Easy to implement and understand

**What happens if not used/alternatives:**
- **HTTP Polling**: High server load, delayed updates, bandwidth waste
- **Server-Sent Events (SSE)**: One-way communication only, HTTP overhead
- **Long Polling**: Complex implementation, resource intensive
- **Flask/Django Views**: Not real-time, poor user experience for live data

---

### 2. WebSocket Handshake Process

**What is this?**
- HTTP upgrade mechanism to establish WebSocket connection
- Protocol negotiation between client and server
- Security validation through key exchange

**Why do we use it?**
- Ensure compatible protocol versions between client and server
- Validate connection authenticity and prevent hijacking
- Negotiate extensions and subprotocols
- Maintain backward compatibility with HTTP infrastructure

**How is it used?**
```python
# Manual WebSocket handshake implementation (educational purposes)
import socket
import hashlib
import base64
import struct

class WebSocketHandshake:
    WEBSOCKET_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    
    @staticmethod
    def generate_accept_key(client_key):
        """Generate WebSocket accept key from client key"""
        combined = client_key + WebSocketHandshake.WEBSOCKET_MAGIC_STRING
        sha1_hash = hashlib.sha1(combined.encode()).digest()
        return base64.b64encode(sha1_hash).decode()
    
    @staticmethod
    def parse_handshake_request(request):
        """Parse WebSocket handshake request"""
        lines = request.split('\r\n')
        headers = {}
        
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return headers
    
    @staticmethod
    def create_handshake_response(client_key):
        """Create WebSocket handshake response"""
        accept_key = WebSocketHandshake.generate_accept_key(client_key)
        
        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key}\r\n"
            "\r\n"
        )
        return response.encode()

# Example usage
def manual_websocket_server():
    """Manual WebSocket server implementation"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8766))
    server_socket.listen(1)
    
    print("Manual WebSocket server listening on localhost:8766")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        
        # Receive handshake request
        request = client_socket.recv(1024).decode()
        print("Handshake request received")
        
        # Parse request headers
        headers = WebSocketHandshake.parse_handshake_request(request)
        client_key = headers.get('sec-websocket-key')
        
        if client_key:
            # Send handshake response
            response = WebSocketHandshake.create_handshake_response(client_key)
            client_socket.send(response)
            print("Handshake completed successfully")
        
        client_socket.close()
        break
```

**Benefits:**
- **Security**: Prevents connection hijacking and CSRF attacks
- **Compatibility**: Works with existing HTTP infrastructure
- **Negotiation**: Allows protocol and extension negotiation
- **Validation**: Ensures proper WebSocket support

**What happens if not used/alternatives:**
- **Direct TCP**: Complex implementation, no HTTP compatibility
- **Custom Protocols**: Firewall issues, complex proxy handling
- **Insecure Connections**: Vulnerable to hijacking and attacks
- **No Negotiation**: Compatibility issues between implementations

---

### 3. WebSocket vs HTTP Communication

**What is this?**
- Comparison between persistent WebSocket connections and stateless HTTP
- Different communication patterns and use cases
- Performance and resource utilization differences

**Why important?**
- Choose appropriate protocol for specific use cases
- Understand performance implications of each approach
- Design efficient communication architecture
- Balance between complexity and performance

**How they differ:**
```python
# HTTP Request/Response Pattern
import requests
import time
import asyncio

class HTTPPoller:
    def __init__(self, url, interval=1):
        self.url = url
        self.interval = interval
        self.running = False
    
    def start_polling(self):
        """Start HTTP polling for data"""
        self.running = True
        while self.running:
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    data = response.json()
                    print(f"HTTP Data received: {data}")
                else:
                    print(f"HTTP Error: {response.status_code}")
            except requests.RequestException as e:
                print(f"HTTP Request failed: {e}")
            
            time.sleep(self.interval)
    
    def stop_polling(self):
        self.running = False

# WebSocket Real-time Pattern
class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
    
    async def connect(self):
        """Connect to WebSocket server"""
        self.websocket = await websockets.connect(self.uri)
        print("WebSocket connected")
    
    async def listen(self):
        """Listen for messages from server"""
        if not self.websocket:
            await self.connect()
        
        try:
            async for message in self.websocket:
                print(f"WebSocket Data received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
    
    async def send_message(self, message):
        """Send message to server"""
        if self.websocket:
            await self.websocket.send(message)

# Performance comparison
import threading
import time

def compare_performance():
    """Compare HTTP polling vs WebSocket performance"""
    
    # HTTP Polling Performance
    start_time = time.time()
    http_requests = 0
    
    def http_simulation():
        nonlocal http_requests
        for _ in range(100):  # Simulate 100 requests
            # Simulate HTTP overhead
            time.sleep(0.01)  # Network + processing time
            http_requests += 1
    
    http_thread = threading.Thread(target=http_simulation)
    http_thread.start()
    http_thread.join()
    
    http_time = time.time() - start_time
    print(f"HTTP: {http_requests} requests in {http_time:.2f}s")
    
    # WebSocket Performance
    start_time = time.time()
    websocket_messages = 0
    
    def websocket_simulation():
        nonlocal websocket_messages
        for _ in range(100):  # Simulate 100 messages
            # Simulate WebSocket overhead (much lower)
            time.sleep(0.001)  # Minimal overhead
            websocket_messages += 1
    
    ws_thread = threading.Thread(target=websocket_simulation)
    ws_thread.start()
    ws_thread.join()
    
    websocket_time = time.time() - start_time
    print(f"WebSocket: {websocket_messages} messages in {websocket_time:.2f}s")
    print(f"WebSocket is {http_time/websocket_time:.1f}x faster")

# compare_performance()
```

**Benefits:**
- **WebSocket Advantages**: Persistent connection, real-time updates, lower latency
- **HTTP Advantages**: Stateless, caching, REST compliance, simpler debugging
- **Resource Usage**: WebSocket uses fewer resources for frequent communication
- **Scalability**: Different scaling patterns for each approach

**What happens if wrong choice:**
- **WebSocket for Rare Updates**: Unnecessary resource usage
- **HTTP for Real-time**: Poor user experience, high server load
- **Inappropriate Protocol**: Performance issues, complex implementation
- **Mixed Approaches**: Inconsistent user experience

---

### 4. WebSocket Message Types and Frames

**What is this?**
- Different types of WebSocket frames: text, binary, control frames
- Frame structure and encoding mechanisms
- Message fragmentation and reassembly

**Why do we use it?**
- Support different data types and formats
- Enable control operations (ping, pong, close)
- Handle large messages through fragmentation
- Optimize bandwidth usage with appropriate encoding

**How is it used?**
```python
import asyncio
import websockets
import json
import pickle
import struct
import base64
from enum import Enum

class MessageType(Enum):
    TEXT = "text"
    JSON = "json"
    BINARY = "binary"
    PING = "ping"
    PONG = "pong"

class WebSocketMessageHandler:
    def __init__(self):
        self.message_handlers = {
            MessageType.TEXT: self.handle_text_message,
            MessageType.JSON: self.handle_json_message,
            MessageType.BINARY: self.handle_binary_message,
            MessageType.PING: self.handle_ping_message,
            MessageType.PONG: self.handle_pong_message,
        }
    
    async def send_text_message(self, websocket, message):
        """Send text message"""
        await websocket.send(message)
        print(f"Sent text: {message}")
    
    async def send_json_message(self, websocket, data):
        """Send JSON message"""
        json_message = json.dumps(data)
        await websocket.send(json_message)
        print(f"Sent JSON: {data}")
    
    async def send_binary_message(self, websocket, data):
        """Send binary message"""
        # Serialize Python object to binary
        binary_data = pickle.dumps(data)
        await websocket.send(binary_data)
        print(f"Sent binary data: {len(binary_data)} bytes")
    
    async def send_ping(self, websocket, payload=b""):
        """Send ping frame"""
        await websocket.ping(payload)
        print("Sent ping")
    
    async def handle_text_message(self, message):
        """Handle received text message"""
        print(f"Received text: {message}")
        return f"Echo: {message}"
    
    async def handle_json_message(self, message):
        """Handle received JSON message"""
        try:
            data = json.loads(message)
            print(f"Received JSON: {data}")
            return {"status": "received", "data": data}
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return {"error": "Invalid JSON"}
    
    async def handle_binary_message(self, message):
        """Handle received binary message"""
        try:
            data = pickle.loads(message)
            print(f"Received binary object: {data}")
            return {"status": "binary_received", "type": str(type(data))}
        except Exception as e:
            print(f"Error processing binary data: {e}")
            return {"error": "Binary processing failed"}
    
    async def handle_ping_message(self, websocket, message):
        """Handle ping message"""
        print("Received ping, sending pong")
        await websocket.pong(message)
    
    async def handle_pong_message(self, message):
        """Handle pong message"""
        print(f"Received pong: {message}")

# Advanced WebSocket Server with message type handling
class AdvancedWebSocketServer:
    def __init__(self, host="localhost", port=8767):
        self.host = host
        self.port = port
        self.clients = set()
        self.message_handler = WebSocketMessageHandler()
    
    async def register_client(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        print(f"Client registered. Total clients: {len(self.clients)}")
    
    async def unregister_client(self, websocket):
        """Unregister client"""
        self.clients.discard(websocket)
        print(f"Client unregistered. Total clients: {len(self.clients)}")
    
    async def broadcast_to_all(self, message, exclude=None):
        """Broadcast message to all clients except excluded one"""
        if self.clients:
            clients_to_send = self.clients - {exclude} if exclude else self.clients
            await asyncio.gather(
                *[client.send(message) for client in clients_to_send],
                return_exceptions=True
            )
    
    async def handle_client(self, websocket, path):
        """Handle individual client connection"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            print("Client connection closed")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def process_message(self, websocket, message):
        """Process received message based on type"""
        try:
            # Determine message type
            if isinstance(message, str):
                # Try to parse as JSON first
                try:
                    json.loads(message)
                    response = await self.message_handler.handle_json_message(message)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    # Handle as text
                    response = await self.message_handler.handle_text_message(message)
                    await websocket.send(response)
            
            elif isinstance(message, bytes):
                # Handle binary message
                response = await self.message_handler.handle_binary_message(message)
                await websocket.send(json.dumps(response))
            
            # Broadcast to other clients
            await self.broadcast_to_all(f"Broadcast: {message}", exclude=websocket)
            
        except Exception as e:
            error_response = {"error": f"Message processing failed: {str(e)}"}
            await websocket.send(json.dumps(error_response))
    
    async def start_server(self):
        """Start the WebSocket server"""
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            ping_interval=20,  # Send ping every 20 seconds
            ping_timeout=10,   # Wait 10 seconds for pong
        )
        print(f"Advanced WebSocket server started on ws://{self.host}:{self.port}")
        await server.wait_closed()

# Client example with different message types
class AdvancedWebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.message_handler = WebSocketMessageHandler()
    
    async def connect(self):
        """Connect to WebSocket server"""
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")
    
    async def send_various_messages(self):
        """Send different types of messages"""
        if not self.websocket:
            return
        
        # Send text message
        await self.message_handler.send_text_message(
            self.websocket, 
            "Hello, this is a text message!"
        )
        
        # Send JSON message
        await self.message_handler.send_json_message(
            self.websocket,
            {"type": "user_message", "content": "Hello World", "timestamp": "2024-01-01"}
        )
        
        # Send binary message
        complex_data = {
            "numbers": [1, 2, 3, 4, 5],
            "nested": {"key": "value"},
            "binary_data": b"some binary content"
        }
        await self.message_handler.send_binary_message(self.websocket, complex_data)
        
        # Send ping
        await self.message_handler.send_ping(self.websocket, b"ping_payload")
    
    async def listen_for_messages(self):
        """Listen for incoming messages"""
        if not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                print(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

# Usage example
async def run_advanced_example():
    # Start server (in practice, this would be in a separate process)
    server = AdvancedWebSocketServer()
    server_task = asyncio.create_task(server.start_server())
    
    # Wait a bit for server to start
    await asyncio.sleep(1)
    
    # Connect client and send messages
    client = AdvancedWebSocketClient("ws://localhost:8767")
    await client.connect()
    await client.send_various_messages()
    
    # Listen for responses briefly
    listen_task = asyncio.create_task(client.listen_for_messages())
    await asyncio.sleep(2)
    listen_task.cancel()

# asyncio.run(run_advanced_example())
```

**Benefits:**
- **Flexibility**: Support multiple data formats and types
- **Efficiency**: Optimal encoding for different data types
- **Control**: Ping/pong for connection health monitoring
- **Reliability**: Message fragmentation for large payloads

**What happens if not used/alternatives:**
- **Single Format**: Limited data exchange capabilities
- **No Health Check**: Undetected connection failures
- **Large Messages**: Memory issues, connection timeouts
- **Poor Encoding**: Inefficient bandwidth usage

---

### 5. WebSocket Authentication and Security

**What is this?**
- Security mechanisms for WebSocket connections
- Authentication strategies and token validation
- Protection against common WebSocket vulnerabilities

**Why do we use it?**
- Protect against unauthorized access and data breaches
- Ensure secure communication channels
- Validate user identity and permissions
- Meet compliance and security requirements

**How is it used?**
```python
import asyncio
import websockets
import jwt
import json
import hashlib
import hmac
import time
from functools import wraps
from typing import Dict, Optional

# JWT-based authentication
class WebSocketAuth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.authenticated_clients = {}  # websocket -> user_info
    
    def generate_token(self, user_id: str, user_data: Dict) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'user_data': user_data,
            'exp': int(time.time()) + 3600,  # 1 hour expiration
            'iat': int(time.time())
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return user info"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
    
    async def authenticate_websocket(self, websocket, path):
        """Authenticate WebSocket connection"""
        try:
            # Get token from query parameters or headers
            query_params = websocket.request_headers.get('Authorization', '')
            if query_params.startswith('Bearer '):
                token = query_params[7:]  # Remove 'Bearer ' prefix
            else:
                # Try to get token from path
                if '?' in path and 'token=' in path:
                    token = path.split('token=')[1].split('&')[0]
                else:
                    await websocket.close(code=4001, reason="No authentication token")
                    return False
            
            # Verify token
            user_info = self.verify_token(token)
            if not user_info:
                await websocket.close(code=4001, reason="Invalid or expired token")
                return False
            
            # Store authenticated user info
            self.authenticated_clients[websocket] = user_info
            print(f"User {user_info['user_id']} authenticated successfully")
            return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            await websocket.close(code=4001, reason="Authentication failed")
            return False
    
    def get_user_info(self, websocket):
        """Get authenticated user info for websocket"""
        return self.authenticated_clients.get(websocket)
    
    def remove_client(self, websocket):
        """Remove client from authenticated clients"""
        self.authenticated_clients.pop(websocket, None)

# Secure WebSocket Server with authentication
class SecureWebSocketServer:
    def __init__(self, secret_key: str, host="localhost", port=8768):
        self.host = host
        self.port = port
        self.auth = WebSocketAuth(secret_key)
        self.clients_by_user = {}  # user_id -> set of websockets
    
    async def register_authenticated_client(self, websocket):
        """Register authenticated client"""
        user_info = self.auth.get_user_info(websocket)
        if user_info:
            user_id = user_info['user_id']
            if user_id not in self.clients_by_user:
                self.clients_by_user[user_id] = set()
            self.clients_by_user[user_id].add(websocket)
            print(f"Registered authenticated client for user {user_id}")
    
    async def unregister_client(self, websocket):
        """Unregister client"""
        user_info = self.auth.get_user_info(websocket)
        if user_info:
            user_id = user_info['user_id']
            if user_id in self.clients_by_user:
                self.clients_by_user[user_id].discard(websocket)
                if not self.clients_by_user[user_id]:
                    del self.clients_by_user[user_id]
        
        self.auth.remove_client(websocket)
    
    async def send_to_user(self, user_id: str, message: str):
        """Send message to specific user (all their connections)"""
        if user_id in self.clients_by_user:
            clients = self.clients_by_user[user_id].copy()
            await asyncio.gather(
                *[client.send(message) for client in clients],
                return_exceptions=True
            )
    
    async def broadcast_to_authenticated(self, message: str, exclude_user=None):
        """Broadcast message to all authenticated users"""
        all_clients = set()
        for user_id, clients in self.clients_by_user.items():
            if user_id != exclude_user:
                all_clients.update(clients)
        
        if all_clients:
            await asyncio.gather(
                *[client.send(message) for client in all_clients],
                return_exceptions=True
            )
    
    async def handle_secure_message(self, websocket, message):
        """Handle message with user context"""
        user_info = self.auth.get_user_info(websocket)
        if not user_info:
            await websocket.send(json.dumps({"error": "Not authenticated"}))
            return
        
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'private_message':
                target_user = data.get('target_user')
                content = data.get('content')
                
                if target_user and content:
                    private_msg = {
                        "type": "private_message",
                        "from": user_info['user_id'],
                        "content": content,
                        "timestamp": int(time.time())
                    }
                    await self.send_to_user(target_user, json.dumps(private_msg))
            
            elif message_type == 'broadcast':
                content = data.get('content')
                if content:
                    broadcast_msg = {
                        "type": "broadcast",
                        "from": user_info['user_id'],
                        "content": content,
                        "timestamp": int(time.time())
                    }
                    await self.broadcast_to_authenticated(
                        json.dumps(broadcast_msg), 
                        exclude_user=user_info['user_id']
                    )
            
            else:
                await websocket.send(json.dumps({"error": "Unknown message type"}))
        
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON message"}))
        except Exception as e:
            await websocket.send(json.dumps({"error": f"Message handling failed: {str(e)}"}))
    
    async def handle_client(self, websocket, path):
        """Handle authenticated client connection"""
        # Authenticate the connection
        if not await self.auth.authenticate_websocket(websocket, path):
            return
        
        await self.register_authenticated_client(websocket)
        
        try:
            # Send welcome message
            user_info = self.auth.get_user_info(websocket)
            welcome_msg = {
                "type": "welcome",
                "message": f"Welcome {user_info['user_id']}!",
                "user_info": user_info['user_data']
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # Handle messages
            async for message in websocket:
                await self.handle_secure_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            print("Authenticated client connection closed")
        except Exception as e:
            print(f"Error handling authenticated client: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self):
        """Start secure WebSocket server"""
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        print(f"Secure WebSocket server started on ws://{self.host}:{self.port}")
        await server.wait_closed()

# Secure WebSocket Client
class SecureWebSocketClient:
    def __init__(self, uri: str, token: str):
        self.uri = uri
        self.token = token
        self.websocket = None
    
    async def connect(self):
        """Connect to secure WebSocket server"""
        # Add token to headers
        extra_headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        try:
            self.websocket = await websockets.connect(
                self.uri,
                extra_headers=extra_headers
            )
            print("Connected to secure WebSocket server")
            return True
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection failed: {e}")
            return False
    
    async def send_private_message(self, target_user: str, content: str):
        """Send private message to another user"""
        if self.websocket:
            message = {
                "type": "private_message",
                "target_user": target_user,
                "content": content
            }
            await self.websocket.send(json.dumps(message))
    
    async def send_broadcast(self, content: str):
        """Send broadcast message"""
        if self.websocket:
            message = {
                "type": "broadcast",
                "content": content
            }
            await self.websocket.send(json.dumps(message))
    
    async def listen(self):
        """Listen for messages"""
        if self.websocket:
            try:
                async for message in self.websocket:
                    data = json.loads(message)
                    print(f"Received: {data}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server")
            except Exception as e:
                print(f"Error listening for