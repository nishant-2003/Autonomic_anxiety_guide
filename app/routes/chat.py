from flask import Blueprint, request
from app import limiter
from app.services.claude_service import claude_service
from app.utils.responses import success, error

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/message", methods=["POST"])
@limiter.limit("30 per minute")
def send_message():
    """
    Send a message to the AI chatbot.

    Request JSON:
        {
            "message": "I've been feeling really anxious lately",
            "session_id": "optional-uuid-for-continuity"
        }

    Response:
        {
            "status": "success",
            "data": {
                "session_id": "...",
                "reply": "...",
                "history_count": 4
            }
        }
    """
    body = request.get_json(silent=True)
    if not body:
        return error("Request body must be JSON.", 400)

    user_message = body.get("message", "").strip()
    if not user_message:
        return error("'message' field is required and cannot be empty.", 400)

    if len(user_message) > 2000:
        return error("Message is too long. Please keep it under 2000 characters.", 400)

    session_id = body.get("session_id")

    try:
        result = claude_service.chat(session_id, user_message)
        return success(result, 200)
    except ValueError as e:
        return error(str(e), 400)
    except Exception as e:
        return error("Failed to get a response. Please try again.", 500)


@chat_bp.route("/session/<session_id>", methods=["GET"])
def get_session(session_id):
    """
    Retrieve chat history for a session.
    """
    from app.models import ChatSession
    session = ChatSession.query.get(session_id)
    if not session:
        return error("Session not found.", 404)

    history = claude_service.get_history(session)
    return success({
        "session_id": session_id,
        "messages": history,
        "count": len(history),
    })


@chat_bp.route("/session/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    """
    Clear all messages in a session (user privacy / reset chat).
    """
    cleared = claude_service.clear_session(session_id)
    if not cleared:
        return error("Session not found.", 404)
    return success({"message": "Session cleared successfully."})
