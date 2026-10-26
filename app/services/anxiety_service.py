"""
Anxiety scoring service.
Implements GAD-7 (Generalized Anxiety Disorder 7-item scale)
and PHQ-4 (ultra-brief anxiety + depression screener).

These are AWARENESS tools — scores are informational only.
Source: Kroenke K, Spitzer RL, Williams JBW, Löwe B (GAD-7, PHQ-4)
"""

GAD7_QUESTIONS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen",
]

PHQ4_QUESTIONS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
]

SCORE_OPTIONS = [
    {"value": 0, "label": "Not at all"},
    {"value": 1, "label": "Several days"},
    {"value": 2, "label": "More than half the days"},
    {"value": 3, "label": "Nearly every day"},
]


def score_gad7(answers: list[int]) -> dict:
    """
    Score a GAD-7 response.
    answers: list of 7 integers, each 0-3
    """
    if len(answers) != 7:
        raise ValueError("GAD-7 requires exactly 7 answers.")
    if not all(0 <= a <= 3 for a in answers):
        raise ValueError("Each answer must be between 0 and 3.")

    total = sum(answers)

    if total <= 4:
        level = "minimal"
        message = "Your responses suggest minimal anxiety. This is the normal range — keep up healthy habits!"
    elif total <= 9:
        level = "mild"
        message = "Your responses suggest mild anxiety. This is very common. Simple coping strategies can help."
    elif total <= 14:
        level = "moderate"
        message = "Your responses suggest moderate anxiety. Consider speaking with a counsellor or trusted person."
    else:
        level = "severe"
        message = "Your responses suggest severe anxiety. We strongly encourage you to speak with a mental health professional."

    return {
        "survey_type": "GAD7",
        "total_score": total,
        "max_score": 21,
        "severity_level": level,
        "message": message,
        "scores_by_question": [
            {"question": GAD7_QUESTIONS[i], "score": answers[i]}
            for i in range(7)
        ],
        "disclaimer": (
            "This is an awareness tool, not a clinical diagnosis. "
            "Scores are for self-reflection only."
        ),
    }


def score_phq4(answers: list[int]) -> dict:
    """
    Score a PHQ-4 response.
    answers: list of 4 integers, each 0-3
    """
    if len(answers) != 4:
        raise ValueError("PHQ-4 requires exactly 4 answers.")
    if not all(0 <= a <= 3 for a in answers):
        raise ValueError("Each answer must be between 0 and 3.")

    total = sum(answers)
    anxiety_score = answers[0] + answers[1]
    depression_score = answers[2] + answers[3]

    if total <= 2:
        level = "normal"
        message = "Your responses are in the normal range. Great!"
    elif total <= 5:
        level = "mild"
        message = "Mild signs detected. Breathing exercises and regular sleep can make a big difference."
    elif total <= 8:
        level = "moderate"
        message = "Moderate signs detected. Speaking with a counsellor could be very helpful."
    else:
        level = "severe"
        message = "Severe signs detected. Please consider reaching out to a mental health professional soon."

    return {
        "survey_type": "PHQ4",
        "total_score": total,
        "max_score": 12,
        "severity_level": level,
        "anxiety_subscale": anxiety_score,
        "depression_subscale": depression_score,
        "message": message,
        "disclaimer": (
            "This is an awareness tool, not a clinical diagnosis. "
            "Scores are for self-reflection only."
        ),
    }


def get_survey_questions(survey_type: str) -> dict:
    """Return questions and options for a given survey type."""
    survey_type = survey_type.upper()
    if survey_type == "GAD7":
        return {
            "survey_type": "GAD7",
            "title": "GAD-7 Anxiety Scale",
            "description": (
                "Over the last 2 weeks, how often have you been bothered by the following problems?"
            ),
            "questions": GAD7_QUESTIONS,
            "options": SCORE_OPTIONS,
        }
    elif survey_type == "PHQ4":
        return {
            "survey_type": "PHQ4",
            "title": "PHQ-4 Quick Check",
            "description": (
                "Over the last 2 weeks, how often have you been bothered by the following problems?"
            ),
            "questions": PHQ4_QUESTIONS,
            "options": SCORE_OPTIONS,
        }
    else:
        raise ValueError(f"Unknown survey type: {survey_type}. Use 'GAD7' or 'PHQ4'.")
