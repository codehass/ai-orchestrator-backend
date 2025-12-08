import os
import requests
from dotenv import load_dotenv

load_dotenv()

categories = [
    "Politics",
    "Economy",
    "Business",
    "Technology",
    "Science",
    "Sports",
    "Health",
    "Environment",
    "Society",
    "Crime",
    "International",
    "Entertainment",
    "Marketing",
    "Culture",
]


def classification_service(text: str, categories_list: list[str]):
    API_URL = (
        "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
    )
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    response = query(
        {
            "inputs": text,
            "parameters": {"candidate_labels": categories_list},
        }
    )[0]

    return {"category": response["label"], "score": response["score"]}
