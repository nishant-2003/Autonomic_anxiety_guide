import requests
import os
from flask import current_app
from app import db
from app.models import ChatSession, ChatMessage

SYSTEM_PROMPT = """You are Calm, a compassionate mental wellness companion for the Autonomic Anxiety Guide — an awareness tool for students and young adults. Help visitors understand anxiety, provide coping strategies, and share wellness tips. You are NOT a therapist. Do not diagnose. If someone mentions crisis, provide: iCall India: 9152987821. Tone: Warm, calm, non-judgmental. Keep responses to 3-5 sentences."""


class ClaudeService:

    def get_or_create_session(self, session_id):
        if session_id:
            session = ChatSession.query.get(session_id)
            if session:
                return session
        session = ChatSession()
        db.session.add(session)
        db.session.commit()
        return session

    def get_history(self, session):
        limit = current_app.config.get("MAX_CHAT_HISTORY", 20)
        messages = (
            session.messages
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )
        return [{"role": m.role, "content": m.content} for m in reversed(messages)]

    def chat(self, session_id, user_message):
        if not user_message or not user_message.strip():
            raise ValueError("Message cannot be empty.")

        session = self.get_or_create_session(session_id)
        history = self.get_history(session)

        api_key = os.environ.get("GROQ_API_KEY")

        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})
        messages_for_api.append({"role": "user", "content": user_message.strip()})

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages_for_api,
                "max_tokens": 512,
            },
            timeout=30,
        )

        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        db.session.add(ChatMessage(
            session_id=session.id,
            role="user",
            content=user_message.strip()
        ))
        db.session.add(ChatMessage(
            session_id=session.id,
            role="assistant",
            content=reply
        ))
        db.session.commit()

        return {
            "session_id": session.id,
            "reply": reply,
            "history_count": len(messages_for_api) + 1,
        }

    def clear_session(self, session_id):
        session = ChatSession.query.get(session_id)
        if not session:
            return False
        ChatMessage.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        return True


claude_service = ClaudeService()