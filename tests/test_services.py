import pytest
from unittest.mock import patch
from app.services.service_gemini import gemini_service, analyzer
from app.services.service_zero_shot import classification_service, categories
from app.schemas.user_schema import GeminiResponse


# ------------------------------------------------------------------
# TEST 1: Mock HuggingFace classification_service
# ------------------------------------------------------------------
@patch("app.services.service_zero_shot.requests.post")
def test_classification_service(mock_post):
    mock_post.return_value.json.return_value = [{"label": "Politics", "score": 0.92}]

    text = "The president announced new policies."
    category, score = classification_service(text, categories)

    assert category == "Politics"
    assert score > 0.7

    mock_post.assert_called_once()


# ------------------------------------------------------------------
# TEST 2: Mock Gemini
# ------------------------------------------------------------------
@patch("app.services.service_gemini.client.models.generate_content")
def test_gemini_service(mock_gemini):

    mock_gemini.return_value.text = """
    {
        "category": "Technology",
        "score": 0.92,
        "summary": "Mock summary",
        "sentiment": "positive"
    }
    """

    response = gemini_service(
        source_text="This is a simple text",
        score=0.92,
        category="Technology",
        response_schema=GeminiResponse,
    )

    assert "positive" in response
    mock_gemini.assert_called_once()


# ------------------------------------------------------------------
# TEST 3: FULL PIPELINE (mock HF + Gemini)
# ------------------------------------------------------------------
@patch("app.services.service_gemini.client.models.generate_content")
@patch("app.services.service_gemini.classification_service")
def test_analyzer(mock_hf, mock_gemini):
    mock_hf.return_value = ("Technology", 0.88)

    mock_gemini.return_value.text = """
    {
        "category": "Technology",
        "score": 0.88,
        "summary": "Pipeline summary",
        "sentiment": "neutral"
    }
    """

    result = analyzer("Some text")

    assert "Technology" in result
    mock_hf.assert_called_once()
    mock_gemini.assert_called_once()
