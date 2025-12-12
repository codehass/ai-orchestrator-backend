from google import genai
from .service_zero_shot import classification_service, categories
from ..schemas.user_schema import GeminiResponse
from ..config import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def gemini_service(source_text: str, score: float, category: str, response_schema):
    prompt = f"""
        You are an AI assistant specialized in generating structured summaries.
        Please summarize the following text in the style of a concise newspaper article or brief. Keep the tone professional, journalistic, and engaging. Title the summary if possible. \n\nText to summarize: {source_text},

        Your task:
        1. Read the provided text.
        2. Use the given classification category and score (from HuggingFace classifier).
        3. Generate a concise and accurate summary.
        4. Follow the response_schema EXACTLY.

        Inputs:
        - Text to summarize: {source_text}
        - Category: {category}
        - Score: {score}

        Output:
        Return ONLY data that respects this schema:
        {response_schema}
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": response_schema.model_json_schema(),
        },
    )

    return response.text


def analyzer(source_text: str):
    category, score = classification_service(source_text, categories)
    return gemini_service(source_text, score, category, GeminiResponse)
