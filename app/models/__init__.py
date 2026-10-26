from datetime import datetime, timezone
from app import db
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class ChatSession(db.Model):
    """
    Represents a visitor's chat session.
    Anonymous — no personal data collected.
    """
    __tablename__ = "chat_sessions"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_active = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    messages = db.relationship(
        "ChatMessage", backref="session", lazy="dynamic",
        cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )

    def to_dict(self):
        return {
            "session_id": self.id,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
        }


class ChatMessage(db.Model):
    """
    Stores individual messages within a session.
    role: 'user' or 'assistant'
    """
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey("chat_sessions.id"), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' | 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


class SurveyResponse(db.Model):
    """
    Stores anonymous GAD-7 / PHQ-4 survey responses.
    Used to generate aggregate awareness statistics — no PII stored.
    """
    __tablename__ = "survey_responses"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=True)  # optional linkage
    survey_type = db.Column(db.String(20), nullable=False)  # 'GAD7' | 'PHQ4'

    # Individual question scores (0-3 each)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=True)  # GAD-7 has 7 questions
    q6 = db.Column(db.Integer, nullable=True)
    q7 = db.Column(db.Integer, nullable=True)

    total_score = db.Column(db.Integer, nullable=False)
    severity_level = db.Column(db.String(20), nullable=False)  # minimal/mild/moderate/severe
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "survey_type": self.survey_type,
            "total_score": self.total_score,
            "severity_level": self.severity_level,
            "created_at": self.created_at.isoformat(),
        }
