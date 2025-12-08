import os
from google import genai
from dotenv import load_dotenv
from .service_zero_shot import classification_service, categories
from ..schemas.user_schema import GeminiResponse

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_service(source_text: str, score: float, category: str, response_schema):
    prompt = f"""
        You are an AI assistant specialized in generating structured summaries.

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


# source_text = """The company announced a new update to its mobile application today.
# The update improves performance, fixes several bugs, and introduces a new dark mode feature.
# Users have reacted positively, saying the app feels faster and easier to use."""


# category, score = classification_service(source_text, categories)

# print(gemini_service(source_text, score, category, GeminiResponse))

# print(analyzer(source_text))


#  hagging face => return category an score of a given text
# Gemini need to get the category from hugging face


# step 1 => get a text, note, paragraph => send it Hugging face => Hugging face will return score and category
# step 2 => transfer the category to Gemini => Gemini will summary the input
# step 3 => Gemini will return a JSON result
# json_result = {
# "category": str
# "score": float
# "summary": str
# "sentiment": str
# }
