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

async def test_client(user_id, action="listen", target=None, message=None, wait_time=3):
    uri = f"ws://localhost:8000/ws/{user_id}"
    async with websockets.connect(uri) as websocket:
        print(f"[{user_id}] Connected")
        
        if action == "block":
            await websocket.send(json.dumps({
                "type": "block",
                "data": {"target_id": target}
            }))
            print(f"[{user_id}] Blocked {target}")
            return

        elif action == "send":
            await websocket.send(json.dumps({
                "type": "message",
                "data": {"recipient_id": target, "content": message}
            }))
            print(f"[{user_id}] Sent to {target}: {message}")

        elif action == "listen":
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=wait_time)
                data = json.loads(msg)
                while data.get("type") != "message":
                    msg = await asyncio.wait_for(websocket.recv(), timeout=wait_time)
                    data = json.loads(msg)
                print(f"[{user_id}] Received: {data.get('content')}")
                return data
            except asyncio.TimeoutError:
                print(f"[{user_id}] No message received (Timeout - Expected if blocked)")
                return None

async def run_tests():
    try:
        print("\n--- Test 4: Blocking ---")
        # 1. Bob blocks Alice
        await test_client("bob", action="block", target="alice")
        
        # 2. Alice sends to Bob
        await asyncio.sleep(0.5)
        # Verify Bob receives nothing
        bob_task = asyncio.create_task(test_client("bob", action="listen", wait_time=3))
        
        await asyncio.sleep(1)
        await test_client("alice", action="send", target="bob", message="Can you hear me?")
        
        res = await bob_task
        if res is None:
            print("Test 4 Passed: Bob blocked Alice's message.")
        else:
            print(f"Test 4 Failed: Bob received message: {res}")
            
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        server_process.kill()
        print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(run_tests())
