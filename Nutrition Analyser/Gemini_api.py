from google import genai
from google.genai import types
import logging
import os
from dotenv import load_dotenv

# Initialize the Gemini API client
load_dotenv()

API_KEY = os.getenv("GROK_API_KEY")

client = genai.Client(api_key=API_KEY)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_food_image(image_path):
    """
    Uses Gemini Vision to analyze the image and detect food items.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    try:
        # Call the model with text + image
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "List all food items in this image, separated by commas.",
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            ],
        )

        # Log the raw response
        logging.debug(f"Gemini API response: {response.text}")

        # Check if the response contains valid text
        if not response.text.strip():
            logging.warning("Empty response from Gemini API.")
            return []

        # Parse text into a list
        text_output = response.text.strip()
        food_items = [item.strip() for item in text_output.split(",") if item.strip()]

        if not food_items:
            logging.warning("No food items detected in the response.")

        return food_items

    except Exception as e:
        logging.error(f"Error while analyzing image: {e}")
        return []
def generate_health_summary(summary):
    try:
        prompt = f"""
        Based on this nutrition data, give short health advice and improvement tips:

        {summary}

        Keep response simple and 3-4 bullet points.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )

        return response.text

    except Exception as e:
        return "Unable to generate AI health summary."
