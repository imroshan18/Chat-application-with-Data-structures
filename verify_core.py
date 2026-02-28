import asyncio
import websockets
import json
import time
import subprocess
import sys
import os

# Start Server
server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "server.main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=os.getcwd(),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("Starting server...")
time.sleep(3) # Wait for server to start

async def test_client(user_id, wait_for_message=False, send_to=None, message=None):
    uri = f"ws://localhost:8000/ws/{user_id}"
    async with websockets.connect(uri) as websocket:
        print(f"[{user_id}] Connected")
        
        if send_to:
            payload = {
                "type": "message",
                "data": {
                    "recipient_id": send_to,
                    "content": message
                }
            }
            await websocket.send(json.dumps(payload))
            print(f"[{user_id}] Sent: {message}")
            
        if wait_for_message:
            msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            data = json.loads(msg)
            print(f"[{user_id}] Received: {data['content']} from {data['sender_id']}")
            return data

async def run_tests():
    try:
        # Test 1: Alice sends to Bob (Bob is online)
        print("\n--- Test 1: Real-time Message ---")
        # Start Bob listener
        bob_task = asyncio.create_task(test_client("bob", wait_for_message=True))
        await asyncio.sleep(1) # Give Bob time to connect
        
        # Alice sends
        await test_client("alice", send_to="bob", message="Hello Bob!")
        
        await bob_task
        print("Test 1 Passed")

        # Test 2: Offline Message
        print("\n--- Test 2: Offline Message ---")
        # Charlie is offline. Alice sends to Charlie.
        await test_client("alice", send_to="charlie", message="Offline msg for Charlie")
        
        # Charlie connects and should receive immediately
        await test_client("charlie", wait_for_message=True)
        print("Test 2 Passed")
        
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        server_process.kill()
        print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(run_tests())
