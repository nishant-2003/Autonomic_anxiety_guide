# 🧠 Autonomic Anxiety Guide — Backend API

A Flask REST API powering the Autonomic Anxiety Guide — an awareness (not diagnostic) tool
for students and young adults, built as a KIIT University 4th Year Major Project.

---

## 📁 Project Structure

```
autonomic-anxiety-guide/
├── app/
│   ├── __init__.py          # App factory (Flask, DB, CORS, rate limiter)
│   ├── models/
│   │   └── __init__.py      # DB models: ChatSession, ChatMessage, SurveyResponse
│   ├── routes/
│   │   ├── chat.py          # /api/chat — AI chatbot endpoints
│   │   ├── survey.py        # /api/survey — GAD-7 / PHQ-4 endpoints
│   │   ├── anxiety.py       # /api/anxiety — facts, coping strategies
│   │   └── resources.py     # /api/resources — helplines, apps, professional help
│   ├── services/
│   │   ├── claude_service.py  # Claude API + conversation memory
│   │   └── anxiety_service.py # Survey scoring logic (GAD-7, PHQ-4)
│   └── utils/
│       └── responses.py     # Standard JSON response helpers
├── tests/
│   └── test_survey.py       # Unit tests for scoring logic
├── config.py                # Dev / Test / Production config
├── run.py                   # App entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚡ Quick Start

### 1. Clone & set up virtual environment
```bash
git clone <your-repo>
cd autonomic-anxiety-guide
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```
Get your API key at: https://console.anthropic.com

### 3. Run the development server
```bash
python run.py
```
API is now live at `http://localhost:5000`

### 4. Run tests
```bash
pytest tests/
```

---

## 🔌 API Reference

### Health Check
```
GET /health
```

---

### 💬 Chat (AI Chatbot)

#### Send a message
```
POST /api/chat/message
Content-Type: application/json

{
  "message": "I've been feeling really anxious about exams",
  "session_id": "optional-uuid"   ← omit on first message
}
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "session_id": "abc-123",
    "reply": "It sounds like exam stress is really weighing on you...",
    "history_count": 2
  }
}
```
> Save `session_id` in the frontend (localStorage) and pass it with every message to maintain memory.

#### Get chat history
```
GET /api/chat/session/{session_id}
```

#### Clear/reset chat
```
DELETE /api/chat/session/{session_id}
```

---

### 📊 Survey

#### Get questions
```
GET /api/survey/questions/GAD7
GET /api/survey/questions/PHQ4
```

#### Submit answers
```
POST /api/survey/submit
Content-Type: application/json

{
  "survey_type": "GAD7",
  "answers": [1, 2, 0, 1, 2, 1, 0],
  "session_id": "optional"
}
```

#### Aggregate stats (for "You're not alone" visualisation)
```
GET /api/survey/stats
```

---

### 🧘 Anxiety Info

```
GET /api/anxiety/facts                  ← prevalence statistics
GET /api/anxiety/coping-strategies      ← breathing, grounding, etc.
GET /api/anxiety/what-is-anxiety        ← educational content
```

---

### 📞 Resources

```
GET /api/resources/helplines            ← Indian crisis helplines
GET /api/resources/professional         ← therapist directories, NHS, etc.
GET /api/resources/apps                 ← Wysa, Headspace, Calm, etc.
GET /api/resources/all                  ← all resources in one call
```

---

## 🤖 How the Chatbot Memory Works

1. First message → backend creates a new `ChatSession` and returns a `session_id`
2. Frontend stores `session_id` in `localStorage`
3. Every subsequent message includes the `session_id`
4. Backend loads last 20 messages from DB and passes them to Claude as conversation history
5. Claude responds with full context of the conversation
6. Both user message and AI reply are saved to the DB

This gives the chatbot persistent, multi-turn memory per visitor — no login required.

---

## 🚀 Production Deployment

### Environment variables to set:
```
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
ANTHROPIC_API_KEY=<your-key>
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://yourdomain.com
```

### Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

### Recommended: Deploy to
- **Render.com** — free tier, easy Flask deploy
- **Railway.app** — simple, generous free tier
- **Heroku** — classic option
- **AWS EC2 / DigitalOcean** — for full control

---

## ⚠️ Disclaimer

This tool is an **awareness resource**, not a clinical diagnostic tool. Survey scores are
for self-reflection only. Always encourage users to seek professional help when needed.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask 3.0 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy via Flask-SQLAlchemy |
| AI | Anthropic Claude API |
| Rate Limiting | Flask-Limiter |
| CORS | Flask-CORS |
| Server | Gunicorn |
