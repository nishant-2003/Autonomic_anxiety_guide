from flask import Blueprint
from app.utils.responses import success

resources_bp = Blueprint("resources", __name__)

HELPLINES = [
    {
        "name": "iCall",
        "country": "India",
        "phone": "9152987821",
        "description": "Psychosocial helpline by TISS, Mumbai. Mon-Sat, 8am-10pm.",
        "website": "https://icallhelpline.org",
    },
    {
        "name": "Vandrevala Foundation",
        "country": "India",
        "phone": "1860-2662-345",
        "description": "24/7 mental health helpline in India.",
        "website": "https://www.vandrevalafoundation.com",
    },
    {
        "name": "Samaritans India",
        "country": "India",
        "phone": "040 4466 0011",
        "description": "Emotional support. Available 24 hours.",
        "website": None,
    },
    {
        "name": "AASRA",
        "country": "India",
        "phone": "9820466627",
        "description": "Crisis intervention centre. 24/7.",
        "website": "http://www.aasra.info",
    },
]

PROFESSIONAL_RESOURCES = [
    {
        "title": "Find a Therapist (India)",
        "url": "https://www.therapize.in",
        "description": "Directory of verified therapists and counsellors in India.",
    },
    {
        "title": "NIMHANS Online Resources",
        "url": "https://nimhans.ac.in",
        "description": "National Institute of Mental Health and Neurosciences, Bangalore.",
    },
    {
        "title": "The Live Love Laugh Foundation",
        "url": "https://thelivelovelaughfoundation.org",
        "description": "Indian foundation for mental health awareness.",
    },
    {
        "title": "NHS — Anxiety Overview",
        "url": "https://www.nhs.uk/mental-health/conditions/generalised-anxiety-disorder/overview/",
        "description": "Clinically reviewed information on GAD from the NHS.",
    },
    {
        "title": "Mind.org.uk",
        "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/",
        "description": "UK charity providing anxiety information and support.",
    },
]

SELF_HELP_APPS = [
    {
        "name": "Wysa",
        "description": "AI-powered mental wellness app, popular in India.",
        "platform": "iOS & Android",
        "url": "https://www.wysa.com",
    },
    {
        "name": "Headspace",
        "description": "Guided meditation and mindfulness exercises.",
        "platform": "iOS & Android",
        "url": "https://www.headspace.com",
    },
    {
        "name": "Calm",
        "description": "Sleep, meditation, and relaxation app.",
        "platform": "iOS & Android",
        "url": "https://www.calm.com",
    },
    {
        "name": "Woebot",
        "description": "CBT-based chatbot for managing anxiety and mood.",
        "platform": "Web & iOS",
        "url": "https://woebothealth.com",
    },
]


@resources_bp.route("/helplines", methods=["GET"])
def get_helplines():
    """Return crisis helpline information."""
    return success(HELPLINES)


@resources_bp.route("/professional", methods=["GET"])
def get_professional():
    """Return links to professional mental health resources."""
    return success(PROFESSIONAL_RESOURCES)


@resources_bp.route("/apps", methods=["GET"])
def get_apps():
    """Return recommended self-help apps."""
    return success(SELF_HELP_APPS)


@resources_bp.route("/all", methods=["GET"])
def get_all():
    """Return all resources in one call."""
    return success({
        "helplines": HELPLINES,
        "professional": PROFESSIONAL_RESOURCES,
        "apps": SELF_HELP_APPS,
    })
