from unittest.mock import patch, MagicMock
from app.services.service_zero_shot import classification_service


@patch("app.services.service_zero_shot.requests.post")
def test_classification_service(mock_post):

    mock_response = MagicMock()
    mock_response.json.return_value = [{"label": "Politics", "score": 0.87}]

    mock_post.return_value = mock_response

    text = "The president announced new policies."
    categories = ["Politics", "Sports"]

    label, score = classification_service(text, categories)

    assert label == "Politics"
    assert score > 0.7
