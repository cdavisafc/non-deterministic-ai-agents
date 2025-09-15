# weather_activities.py

from typing import Any
from temporalio import activity
import httpx
import json
from pydantic import BaseModel
import openai
from helpers import tool_helpers
from pydantic import Field
import random

RANDOM_NUMBER_TOOL_OAI: dict[str, Any] = tool_helpers.oai_responses_tool_from_model(
    "get_random_number",
    "Get a random number between 0 and 100.",
    None)

@activity.defn
async def get_random_number() -> str:
    """Get a random number between 0 and 100.
    """
    data = random.randint(0, 100)
    return str(data)
