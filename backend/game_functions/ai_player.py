import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
import requests
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from backend.game_functions.player import Player


class AIPlayer(Player):
    def __init__(self, name, player_type, location):
        super().__init__(name, player_type, location, is_computer=1)


def move():
    endpoint = "https://gameopenai.openai.azure.com/openai/deployments/gpt-4o-mini-player/chat/completions?api-version=2024-07-18-preview"
    model_name = "gpt-4o-mini"
    api_key = os.getenv("AI_API_KEY")

    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    message = """
        Airports: BIKF, EBBR, EDDB, EFHK, EGLL, EIDW, ENGM, EPWA, ESSA, LBSF, LEMD, LFPG, LGAV, LHBP, LIRF, LKPR, LOWW, LPPT, LROP, LYBE, UKBB
        You: LEMD
        Detectives: EGLL, EFHK
        Tickets: 10x Closest (C), 6x Near (N), 4x Farthest (F)
        Goal: Avoid being caught by the detectives

        Important: Avoid airports close to the detectives. Do not fly directly to or near EGLL or EFHK. Choose an airport that is not near the detectives, even if it means selecting a farther airport.

        Only respond with one ICAO code and the ticket used (C, N, F), one at a time. For example:
        EPWA, C

        Do not list multiple answers. Prioritize staying far from the detectives.
    """

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=message),
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )
    return response