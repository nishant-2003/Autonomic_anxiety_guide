from flask import Blueprint, request
from app import limiter, db
from app.models import SurveyResponse
from app.services.anxiety_service import score_gad7, score_phq4, get_survey_questions
from app.utils.responses import success, error

survey_bp = Blueprint("survey", __name__)


@survey_bp.route("/questions/<survey_type>", methods=["GET"])
def get_questions(survey_type):
    """
    Get survey questions for a given type (GAD7 or PHQ4).

    GET /api/survey/questions/GAD7
    GET /api/survey/questions/PHQ4
    """
    try:
        data = get_survey_questions(survey_type)
        return success(data)
    except ValueError as e:
        return error(str(e), 400)


@survey_bp.route("/submit", methods=["POST"])
@limiter.limit("10 per minute")
def submit_survey():
    """
    Submit survey answers and receive a scored result.

    Request JSON:
        {
            "survey_type": "GAD7",
            "answers": [1, 2, 0, 1, 2, 1, 0],
            "session_id": "optional"
        }

    Response includes score, severity level, and message.
    No personal data is stored.
    """
    body = request.get_json(silent=True)
    if not body:
        return error("Request body must be JSON.", 400)

    survey_type = body.get("survey_type", "").upper()
    answers = body.get("answers")
    session_id = body.get("session_id")

    if not survey_type:
        return error("'survey_type' is required. Use 'GAD7' or 'PHQ4'.", 400)
    if not isinstance(answers, list):
        return error("'answers' must be a list of integers.", 400)

    try:
        if survey_type == "GAD7":
            result = score_gad7(answers)
        elif survey_type == "PHQ4":
            result = score_phq4(answers)
        else:
            return error("Invalid survey_type. Use 'GAD7' or 'PHQ4'.", 400)
    except ValueError as e:
        return error(str(e), 400)

    # Persist anonymised result
    q_vals = answers + [None] * (7 - len(answers))
    record = SurveyResponse(
        session_id=session_id,
        survey_type=survey_type,
        q1=q_vals[0], q2=q_vals[1], q3=q_vals[2], q4=q_vals[3],
        q5=q_vals[4], q6=q_vals[5], q7=q_vals[6],
        total_score=result["total_score"],
        severity_level=result["severity_level"],
    )
    db.session.add(record)
    db.session.commit()

    return success(result, 201)


@survey_bp.route("/stats", methods=["GET"])
def get_stats():
    """
    Aggregate awareness statistics from all survey submissions.
    Used to power the "You're not alone" data visualisation on the frontend.
    """
    from sqlalchemy import func

    stats = {}
    for survey_type in ("GAD7", "PHQ4"):
        total = SurveyResponse.query.filter_by(survey_type=survey_type).count()
        if total == 0:
            stats[survey_type] = {"total_responses": 0}
            continue

        breakdown = (
            db.session.query(
                SurveyResponse.severity_level,
                func.count(SurveyResponse.id).label("count")
            )
            .filter_by(survey_type=survey_type)
            .group_by(SurveyResponse.severity_level)
            .all()
        )

        avg_score = db.session.query(
            func.avg(SurveyResponse.total_score)
        ).filter_by(survey_type=survey_type).scalar()

        stats[survey_type] = {
            "total_responses": total,
            "average_score": round(float(avg_score), 1),
            "severity_breakdown": {row.severity_level: row.count for row in breakdown},
        }

    return success(stats)
