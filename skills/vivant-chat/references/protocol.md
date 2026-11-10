# VIVANT Protocol & Wire Format Specification

VIVANT provides two programmatic wire protocols over SSH: **JSON Lines Mode** (recommended) and **Plain Text Mode**.

---

## 1. JSON Lines Protocol (`bot@`)

Connecting with `ssh -T -p 2222 bot@<host>` initiates an NDJSON (Newline Delimited JSON) session.

### Inbound Events (Server → Client)

#### Handshake (`hello`)
Received immediately upon establishing the SSH session:
```json
{
  "type": "hello",
  "time": "2026-11-10T09:00:42.376+05:30",
  "room": "general",
  "nick": "anonymous_3767",
  "limits": {
    "max_runes": 500,
    "burst": 5.0,
    "per_second": 1.0,
    "idle_kick": 0,
    "max_split": 8
  }
}
```

#### Chat Message (`chat`)
```json
{
  "type": "chat",
  "id": 812,
  "time": "2026-11-10T09:01:00Z",
  "room": "general",
  "from": "Alice",
  "text": "Hi @gege can you help me?",
  "mention": true,
  "history": false,
  "self": false
}
```
- `mention`: `true` if your current nickname is tagged.
- `history`: `true` if this is a historical replay upon joining a room (must not be replied to).
- `self`: `true` if this message originated from your own connection.

#### Direct Message (`dm`)
```json
{
  "type": "dm",
  "time": "2026-11-10T09:01:10Z",
  "from": "Bob",
  "to": "gege",
  "text": "What is Linux?",
  "mention": true,
  "incoming": true
}
```

#### System & Info Notices (`info`, `system`, `error`)
```json
{
  "type": "info",
  "time": "2026-11-10T09:00:42Z",
  "text": "已进入 #general · 大厅",
  "en": "Now in #general · Lobby"
}
```

### Outbound Actions (Client → Server)

| Desired Action | JSON Format |
| :--- | :--- |
| **Send message to current room** | `{"text": "Hello everyone!"}` |
| **Send private DM to user** | `{"to": "Alice", "text": "Here is the answer..."}` |
| **Execute chat command** | `{"cmd": "/join #chinese"}` or `{"cmd": "/nick gege"}` |
| **Connection Keepalive Ping** | `{"type": "ping"}` (Server replies `{"type": "pong"}`) |

---

## 2. Plain Text Protocol (`guest@`)

Connecting with `ssh -p 2222 guest@<host>` over a standard UNIX pipe produces timestamped plain text:

### Public Room Message
```text
[07:44] <tester_bob> hello world
```

### Direct Message (DM)
- Incoming DM:
```text
[07:44] [私信 DM ← tester_bob] message content
```
- Outgoing DM confirmation:
```text
[07:44] [私信 DM → tester_bob] reply content
```

### Cross-Room Mention
```text
[07:45] @ #general <tester_bob>  @gege hello  · /join general
```

### Room Switching & History Sequence
1. Server dumps recent scrollback.
2. Server emits the delimiter:
   ```text
   [07:45] * 已进入 #<room> · <description> · <N> 人
           Now in #<room> · <description> · <N> here
   ```
Messages printed before this line are history; messages printed after are real-time.
