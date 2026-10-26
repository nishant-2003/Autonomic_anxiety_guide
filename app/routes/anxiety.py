from flask import Blueprint
from app.utils.responses import success

anxiety_bp = Blueprint("anxiety", __name__)

# Static awareness data — sourced from NHS / WHO / published research
# In a production app, these could be moved to a DB and admin-editable
ANXIETY_FACTS = [
    {
        "id": 1,
        "stat": "1 in 4",
        "context": "people will experience a mental health problem in any given year",
        "source": "NHS England",
    },
    {
        "id": 2,
        "stat": "284 million",
        "context": "people worldwide live with an anxiety disorder",
        "source": "Our World in Data / GBD 2017",
    },
    {
        "id": 3,
        "stat": "18-25",
        "context": "is the age group most likely to experience anxiety",
        "source": "NIMH, 2023",
    },
    {
        "id": 4,
        "stat": "40%",
        "context": "of college students report overwhelming anxiety",
        "source": "ACHA National College Health Assessment",
    },
    {
        "id": 5,
        "stat": "Only 37%",
        "context": "of people with anxiety receive treatment",
        "source": "Anxiety & Depression Association of America",
    },
]

COPING_STRATEGIES = [
    {
        "id": 1,
        "title": "4-7-8 Breathing",
        "category": "breathing",
        "description": "Inhale for 4 counts, hold for 7, exhale for 8. Activates your parasympathetic nervous system.",
        "steps": [
            "Sit comfortably and close your eyes",
            "Inhale quietly through your nose for 4 seconds",
            "Hold your breath for 7 seconds",
            "Exhale completely through your mouth for 8 seconds",
            "Repeat 3-4 times",
        ],
    },
    {
        "id": 2,
        "title": "5-4-3-2-1 Grounding",
        "category": "grounding",
        "description": "Engages your senses to anchor you to the present moment.",
        "steps": [
            "Name 5 things you can SEE",
            "Name 4 things you can TOUCH",
            "Name 3 things you can HEAR",
            "Name 2 things you can SMELL",
            "Name 1 thing you can TASTE",
        ],
    },
    {
        "id": 3,
        "title": "Progressive Muscle Relaxation",
        "category": "body",
        "description": "Systematically tense and release muscle groups to reduce physical tension.",
        "steps": [
            "Start with your feet — tense for 5 seconds",
            "Release and notice the relaxation for 10 seconds",
            "Move up: calves, thighs, stomach, hands, arms, shoulders, face",
            "End with a full body scan",
        ],
    },
    {
        "id": 4,
        "title": "Journaling",
        "category": "cognitive",
        "description": "Writing down thoughts reduces their intensity and helps identify patterns.",
        "steps": [
            "Set a timer for 10 minutes",
            "Write freely — don't edit yourself",
            "Ask: what triggered this? What's the worst that could happen? How likely is it really?",
            "Write one small action you can take today",
        ],
    },
]

WHAT_IS_ANXIETY = {
    "definition": (
        "Anxiety is your body's natural response to stress or perceived threat. "
        "It's the feeling of fear or apprehension about what's to come. "
        "Some anxiety is normal and even helpful — it keeps you alert. "
        "It becomes a concern when it's excessive, persistent, or interferes with daily life."
    ),
    "physical_symptoms": [
        "Increased heart rate",
        "Rapid breathing or shortness of breath",
        "Sweating",
        "Trembling or shaking",
        "Feeling weak or tired",
        "Difficulty concentrating",
        "Trouble sleeping",
        "Stomach problems",
    ],
    "types": [
        {"name": "Generalised Anxiety Disorder (GAD)", "description": "Persistent, excessive worry about many things"},
        {"name": "Social Anxiety", "description": "Intense fear of social situations or being judged"},
        {"name": "Panic Disorder", "description": "Recurring, unexpected panic attacks"},
        {"name": "Specific Phobias", "description": "Intense fear of a specific object or situation"},
        {"name": "Separation Anxiety", "description": "Excessive fear about being separated from attachment figures"},
    ],
    "when_to_seek_help": (
        "Consider speaking to a professional if anxiety: interferes with daily life, "
        "lasts more than 6 months, causes you to avoid situations, "
        "or is accompanied by depression or substance use."
    ),
}


@anxiety_bp.route("/facts", methods=["GET"])
def get_facts():
    """Return awareness statistics about anxiety prevalence."""
    return success(ANXIETY_FACTS)


@anxiety_bp.route("/coping-strategies", methods=["GET"])
def get_coping_strategies():
    """Return a list of evidence-based coping strategies."""
    return success(COPING_STRATEGIES)


@anxiety_bp.route("/what-is-anxiety", methods=["GET"])
def what_is_anxiety():
    """Return educational content about what anxiety is."""
    return success(WHAT_IS_ANXIETY)
