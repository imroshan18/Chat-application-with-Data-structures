# Real-time Chat with Python & FastAPI

A clean, clear, and efficient real-time chat application designed to demonstrate robust **System Design** and **Data Structure** principles.

## 🚀 Features
- **1:1 Real-time Messaging** (HashMap routing)
- **Offline Messaging** (Deque queuing) 
- **Group Chat** (Set membership)
- **Presence System** (Online/Offline status)
- **Multi-device Support**

## 🛠️ Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server**
   ```bash
   uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Run Client(s)**
   Open multiple terminals:
   ```bash
   # Terminal 1
   python client/client.py alice

   # Terminal 2
   python client/client.py bob
   ```

## 💬 Commands
- **Direct Message**: `@bob Hello!`
- **Join Group**: `/join devs`
- **Group Message**: `#devs Hi Team!`
- **Block User**: `/block alice`
- **Typing Indicator**: `/typing bob`

## 📚 For Verification / Exams
Check `viva_explanation.md` for a detailed breakdown of the internal data structures and architecture logic.
