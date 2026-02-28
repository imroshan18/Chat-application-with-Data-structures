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

async def test_client(user_id, action="listen", group=None, message=None, wait_time=5):
    uri = f"ws://localhost:8000/ws/{user_id}"
    async with websockets.connect(uri) as websocket:
        print(f"[{user_id}] Connected")
        
        if action == "join_and_listen":
            # Join Group
            await websocket.send(json.dumps({
                "type": "group_join",
                "data": {"group_id": group}
            }))
            print(f"[{user_id}] Joined {group}")
            
            # Listen
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=wait_time)
                data = json.loads(msg)
                # Ignore presence events or own join events if broadcasted back
                while data.get("type") != "message":
                    msg = await asyncio.wait_for(websocket.recv(), timeout=wait_time)
                    data = json.loads(msg)
                
                print(f"[{user_id}] Received Group Msg: {data.get('content')}")
                return data
            except asyncio.TimeoutError:
                print(f"[{user_id}] No message received (Timeout)")
                return None

        elif action == "send_group":
            # Join first (optional depending on logic, but usually required to receive, not strictly to send in some implementations, but let's assume valid member)
            await websocket.send(json.dumps({
                "type": "group_join",
                "data": {"group_id": group}
            }))
            await asyncio.sleep(0.5)
            
            # Send
            await websocket.send(json.dumps({
                "type": "group_message",
                "data": {"group_id": group, "content": message}
            }))
            print(f"[{user_id}] Sent to {group}: {message}")

async def run_tests():
    try:
        print("\n--- Test 3: Group Chat ---")
        # Bob joins "devs" and listens
        bob_task = asyncio.create_task(test_client("bob", action="join_and_listen", group="devs", wait_time=5))
        
        await asyncio.sleep(1)
        
        # Alice sends to "devs"
        await test_client("alice", action="send_group", group="devs", message="Hello Devs!")
        
        res = await bob_task
        if res and res.get("content") == "Hello Devs!":
            print("Test 3 Passed: Bob received group message.")
        else:
            print("Test 3 Failed: Bob did not receive correct message.")
            
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        server_process.kill()
        print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(run_tests())
