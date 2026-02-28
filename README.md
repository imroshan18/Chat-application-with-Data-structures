

### Distributed Real-Time Chat System with FastAPI

SyncTalk is a real-time messaging platform built with FastAPI that demonstrates core backend engineering principles including routing efficiency, concurrent communication handling, in-memory data structures, and multi-user coordination.

This project focuses on system design fundamentals rather than UI complexity, showcasing how scalable messaging systems are architected at a structural level.

---

## Author

**imroshan18**

---

## Project Overview

SyncTalk simulates a lightweight distributed chat infrastructure supporting:

* Direct peer-to-peer messaging
* Group communication channels
* Offline message storage
* Presence tracking
* Multi-device connectivity

The system highlights efficient in-memory data structure usage to manage active users, groups, and message queues.

---

## Architectural Design

The application follows a client-server model powered by FastAPI.

### Server Layer (FastAPI)

The backend:

* Manages WebSocket connections
* Routes messages dynamically
* Tracks online presence
* Maintains user relationships
* Handles offline message buffering

---

### Core Data Structures

The system intentionally leverages fundamental data structures for optimized performance:

| Feature             | Data Structure       | Purpose                    |
| ------------------- | -------------------- | -------------------------- |
| Active User Routing | HashMap (Dictionary) | O(1) message delivery      |
| Offline Messages    | Deque                | Efficient queue management |
| Group Membership    | Set                  | Fast membership validation |
| Block List          | Set                  | Instant restriction checks |

This design ensures predictable time complexity and scalable logic.

---

## Key Functionalities

### 1. Direct Messaging

Users can send private messages to another connected user in real time.

### 2. Group Communication

Users can join named groups and broadcast messages to all members.

### 3. Offline Messaging

If a recipient is disconnected:

* Messages are queued
* Delivered upon reconnection

### 4. Presence Tracking

The system monitors:

* Online status
* Disconnections
* Reconnection events

### 5. User Blocking

Prevents unwanted communication through fast membership validation.

### 6. Typing Indicators

Simulates real-time user activity awareness.

---

## Technology Stack

| Component              | Technology  |
| ---------------------- | ----------- |
| Backend Framework      | FastAPI     |
| Communication Protocol | WebSockets  |
| Concurrency            | AsyncIO     |
| Language               | Python 3.8+ |

---

## Installation Guide

### 1. Install Dependencies

```bash id="e9s2am"
pip install -r requirements.txt
```

---

### 2. Run the Server

```bash id="h2r0mn"
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at:

```id="p9q2lm"
http://localhost:8000
```

---

### 3. Run Client Instances

Open multiple terminals:

```bash id="x4q1va"
python client/client.py alice
```

```bash id="y7d8vk"
python client/client.py bob
```

Each client simulates an independent user session.

---

## Command Reference

### Direct Message

```
@username Hello!
```

### Join Group

```
/join groupname
```

### Send Group Message

```
#groupname Message text
```

### Block User

```
/block username
```

### Typing Indicator

```
/typing username
```

---

## System Workflow

1. User connects via WebSocket.
2. Server registers user in active connection map.
3. Messages are parsed for command type:

   * Direct
   * Group
   * System command
4. Routing logic determines delivery path.
5. If recipient offline → enqueue message.
6. Upon reconnection → flush queued messages.

---

## Project Structure

```id="l3q8dm"
SyncTalk/
│
├── server/
│   ├── main.py
│   ├── routing.py
│   ├── connection_manager.py
│
├── client/
│   ├── client.py
│
├── verify_block.py
├── verify_core.py
├── verify_groups.py
├── check_db.py
├── requirements.txt
└── README.md
```

---

## Design Goals

* Emphasize clean routing logic
* Demonstrate real-time asynchronous communication
* Showcase efficient data structure usage
* Simulate scalable messaging architecture
* Maintain minimal external dependencies

---

## Possible Enhancements

* Persistent database storage
* JWT authentication
* Horizontal scaling via Redis Pub/Sub
* Docker containerization
* Web-based frontend UI
* End-to-end encryption

---

## Professional Positioning

This project demonstrates strong understanding of:

* WebSocket communication
* Backend concurrency
* Data structure optimization
* Real-time system design
* FastAPI service architecture

It is particularly relevant for roles in:

* Backend Development
* Systems Engineering
* Distributed Systems
* Real-Time Application Development

