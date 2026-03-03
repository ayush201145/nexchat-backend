# ⚡ NexChat — AI-Powered Real-Time Chat Application

A production-grade full-stack messaging platform with intelligent smart reply suggestions, role-based admin moderation, and WebSocket-driven real-time communication.

---

## 🏗️ Architecture Overview

```
nexchat/
├── server/            # Node.js + Express + Socket.io + MongoDB
│   ├── server.js      # Main backend (REST API + WebSocket events)
│   ├── package.json
│   └── .env.example
│
├── client/            # React frontend
│   └── src/
│       └── App.jsx    # Full SPA: Auth, Chat UI, Admin Dashboard
│
└── ml-service/        # Python Flask + Scikit-Learn
    ├── app.py         # Naive Bayes NLP model for smart replies
    └── requirements.txt
```

### Tech Stack

| Layer         | Technology                               |
|---------------|------------------------------------------|
| Frontend      | React 18, Socket.io-client, CSS-in-JS    |
| Backend API   | Node.js, Express.js                      |
| Real-Time     | Socket.io (WebSocket protocol)           |
| Database      | MongoDB + Mongoose ODM                   |
| Auth          | JWT (jsonwebtoken) + bcryptjs            |
| ML Service    | Python Flask, Scikit-Learn, NumPy        |
| NLP Model     | Multinomial Naive Bayes + TF-IDF         |

---

## 🚀 Getting Started

### Prerequisites
- Node.js ≥ 18
- Python ≥ 3.9
- MongoDB (local or Atlas)

---

### 1. Start the Backend (Node.js)

```bash
cd server
cp .env.example .env          # Edit with your settings
npm install
npm run dev                   # Starts on http://localhost:5000
```

---

### 2. Start the ML Service (Python)

```bash
cd ml-service
pip install -r requirements.txt
python app.py                 # Starts on http://localhost:5001
```

The Naive Bayes model trains automatically on startup (~200ms). A trained model is cached to `smart_reply_model.pkl` and reused on subsequent runs.

---

### 3. Start the React Frontend

```bash
cd client
npm install
npm start                     # Opens http://localhost:3000
```

---

## 🧠 ML Model — Naive Bayes Smart Replies

### How It Works

```
User receives message
        │
        ▼
Text Preprocessing
(lowercase → remove URLs → strip punctuation → normalize whitespace)
        │
        ▼
TF-IDF Vectorizer (unigrams + bigrams, max 5000 features)
        │
        ▼
Multinomial Naive Bayes Classifier
        │
        ▼
Predict intent class (greeting/question/agree/gratitude/...)
        │
        ▼
Map to reply templates → Return top 3 suggestions
```

### Intent Classes

| Class        | Example Triggers              | Reply Suggestions                      |
|--------------|-------------------------------|----------------------------------------|
| greeting     | "hello", "hey", "good morning" | "Hey! 👋", "Hello there!", "Hi!"       |
| farewell     | "bye", "see you later"        | "See you! 👋", "Bye! Take care!"       |
| agree        | "yes", "absolutely", "totally" | "Totally agree! 🙌", "100%!"          |
| question     | "how are you", "can you help" | "Great question!", "Let me check!"     |
| gratitude    | "thank you", "thanks"         | "You're welcome! 😊", "Happy to help!" |
| apology      | "sorry", "my bad"             | "No worries! 😊", "It's okay!"         |
| positive     | "great job", "awesome"        | "Thanks! 😊", "Appreciate it! 🙏"     |

### Retrain with Custom Data

```bash
curl -X POST http://localhost:5001/train \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {"text": "see you tomorrow", "label": "farewell"},
      {"text": "sounds perfect", "label": "agree"}
    ]
  }'
```

---

## 🔌 WebSocket Events

### Client → Server

| Event          | Payload                    | Description                  |
|----------------|----------------------------|------------------------------|
| `room:join`    | `{ room: string }`         | Join a chat room             |
| `room:leave`   | `{ room: string }`         | Leave a chat room            |
| `message:send` | `{ room, content }`        | Send a message               |
| `typing:start` | `{ room: string }`         | Broadcast typing started     |
| `typing:stop`  | `{ room: string }`         | Broadcast typing stopped     |

### Server → Client

| Event            | Payload                          | Description                  |
|------------------|----------------------------------|------------------------------|
| `room:history`   | `Message[]`                      | Last 50 messages on join     |
| `message:new`    | `Message`                        | New real-time message        |
| `message:system` | `{ content, type: 'system' }`   | Join/leave notifications     |
| `typing:update`  | `{ username, isTyping }`        | Typing indicator update      |
| `user:online`    | `{ userId, username }`          | User came online             |
| `user:offline`   | `{ userId }`                    | User went offline            |

---

## 🔑 REST API Endpoints

### Auth
```
POST /api/auth/register   { username, email, password }
POST /api/auth/login      { email, password }
```

### Chat
```
GET  /api/rooms              → List public rooms
POST /api/rooms              → Create room
GET  /api/messages/:room     → Last 100 messages
POST /api/smart-reply        { message } → Get 3 AI suggestions
```

### Admin (role: admin only)
```
GET    /api/admin/stats              → Platform stats
GET    /api/admin/users              → All users
PATCH  /api/admin/users/:id/ban     { ban: boolean }
GET    /api/admin/flagged            → Flagged messages
DELETE /api/admin/messages/:id      → Delete message
```

---

## ⚙️ Admin Dashboard

Access the admin panel by logging in with a user that has `role: "admin"` in MongoDB. Features:

- **Overview** — Live stats: total users, online count, messages, rooms, flagged content
- **User Management** — View all users, ban/unban accounts
- **Content Moderation** — Review auto-flagged messages, delete violations

To create an admin user, manually update the `role` field in MongoDB:
```js
db.users.updateOne({ email: "you@example.com" }, { $set: { role: "admin" } })
```

---

## 🔒 Security Features

- Passwords hashed with bcryptjs (12 salt rounds)
- JWT authentication with 7-day expiry
- Socket.io auth middleware validates tokens on every connection
- Auto-flagging for keywords (extensible with real NLP pipeline)
- Admin-only API routes protected by role middleware
- Banned users blocked at login

---

## 📈 Potential Enhancements

- Swap Naive Bayes for a transformer model (BERT/DistilBERT)
- Add end-to-end encryption for DMs
- Implement read receipts and message reactions
- Add file/image upload support via S3
- Deploy with Docker Compose for all 3 services
- Add Redis for caching online users and session management
