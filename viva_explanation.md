# Real-time Chat Application - Viva & Interview Guide

## 🏗️ System Architecture
This project is a high-performance, real-time messaging system built with **FastAPI** (Backend) and **WebSockets** (Protocol). 

### Key Characteristics:
1.  **Event-Driven**: Uses WebSocket events (`message`, `group_join`, `presence`) for real-time interaction.
2.  **In-Memory State**: Uses optimized data structures for sub-millisecond latency.
3.  **Explainable Design**: Every data structure choice is justified by Big-O analysis.

---

## 🧠 Data Structure Justification (The "Why")

| Feature | Data Structure | Time Complexity | Logical Justification |
| :--- | :--- | :--- | :--- |
| **Active Connections** | `HashMap<UserId, List[WebSocket]>` | **O(1) Access** | Instant lookup of a user's active sockets. `List` handles multiple devices (Laptop + Phone) simultaneously. |
| **Presence System** | `Set<UserId>` | **O(1) Check** | `if user in online_users` is faster than checking Dict keys. Sets ensure uniqueness automatically. |
| **Offline Messages** | `HashMap<UserId, Deque<Message>>` | **O(1) Append/Pop** | `Deque` (Double Ended Queue) allows O(1) addition to the end and O(1) removal from the front (FIFO). A standard List is O(N) for popping from front. |
| **Group Members** | `HashMap<GroupId, Set<UserId>>` | **O(1) Member Check** | `Set` prevents duplicate members and allows instant verification if a user is allowed to post in a group. |
| **Blocked Users** | `HashMap<UserId, Set<UserId>>` | **O(1) Access** | `Set` allows O(1) checking `if sender in blocked_users[recipient]`. Efficient for every message lookup. |

---

## 🚀 Scaling & Cloud (Future Scope)
**Interviewer:** "How would you scale this to 1 Million users?"

**Answer:**
1.  **State Management**: Move `active_connections` map to **Redis** (Distributed Key-Value Store).
2.  **Message Queue**: Use **RabbitMQ** or **Kafka** to handle message bursts.
3.  **Database**: Store chat history (persist `Deque` contents) in **Cassandra** (Write-heavy) or **PostgreSQL**.
4.  **Load Balancing**: Use **Nginx** to distribute WebSocket connections across multiple FastAPI workers.

---

## 🧵 Message Flow
1.  **User A sends Message**: Client sends JSON `{"type": "message", "to": "B"}`.
2.  **Server Routing**:
    - Looks up B in `active_connections` (O(1)).
    - **If Online**: Iterates B's sockets and sends immediate push.
    - **If Offline**: Pushes to `offline_messages[B]` (O(1)).
3.  **User B Connects**:
    - Server checks `offline_messages[B]`.
    - Flushes Deque to B's socket.

## 🏃 Connectivity Modes
1.  **Localhost**: multiple terminals, same machine.
2.  **LAN**: Run server on `0.0.0.0`, clients connect to IP.
3.  **Ngrok**: Expose port 8000 via ngrok, clients connect from anywhere.
