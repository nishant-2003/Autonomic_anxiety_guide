import pytest
from app.services.anxiety_service import score_gad7, score_phq4, get_survey_questions


def test_gad7_minimal():
    result = score_gad7([0, 0, 0, 0, 0, 0, 0])
    assert result["total_score"] == 0
    assert result["severity_level"] == "minimal"


def test_gad7_mild():
    result = score_gad7([1, 1, 1, 1, 1, 1, 1])
    assert result["total_score"] == 7
    assert result["severity_level"] == "mild"


def test_gad7_moderate():
    result = score_gad7([2, 2, 2, 2, 2, 0, 0])
    assert result["total_score"] == 10
    assert result["severity_level"] == "moderate"


def test_gad7_severe():
    result = score_gad7([3, 3, 3, 3, 3, 3, 3])
    assert result["total_score"] == 21
    assert result["severity_level"] == "severe"


def test_gad7_wrong_length():
    with pytest.raises(ValueError):
        score_gad7([1, 2, 3])


def test_gad7_out_of_range():
    with pytest.raises(ValueError):
        score_gad7([4, 0, 0, 0, 0, 0, 0])


def test_phq4_normal():
    result = score_phq4([0, 0, 0, 0])
    assert result["total_score"] == 0
    assert result["severity_level"] == "normal"


def test_phq4_severe():
    result = score_phq4([3, 3, 3, 3])
    assert result["total_score"] == 12
    assert result["severity_level"] == "severe"


def test_phq4_subscales():
    result = score_phq4([2, 1, 3, 0])
    assert result["anxiety_subscale"] == 3
    assert result["depression_subscale"] == 3


def test_get_questions_gad7():
    data = get_survey_questions("GAD7")
    assert len(data["questions"]) == 7


def test_get_questions_phq4():
    data = get_survey_questions("PHQ4")
    assert len(data["questions"]) == 4


def test_get_questions_invalid():
    with pytest.raises(ValueError):
        get_survey_questions("INVALID")
