from openai.lib._pydantic import to_strict_json_schema  # private API; may change
# there currently is no public API to generate the tool definition from a Pydantic model
# or a function signature.
from pydantic import BaseModel

def oai_responses_tool_from_model(name: str, description: str, model: type[BaseModel]):
    return {
        "type": "function",
        "name": name,
        "description": description,
        # OpenAI Responses strict tools require a JSON Schema object where
        # additionalProperties is explicitly false. For tools without
        # parameters, supply an empty object schema.
        "parameters": (
            to_strict_json_schema(model)
            if model
            else {"type": "object", "properties": {}, "required": [], "additionalProperties": False}
        ),
        "strict": True,
    }

CHAOTIC_AGENT_SYSTEM_INSTRUCTIONS = """
You are a chaotic agent that does things in a way that seemingly has no rhyme or reason.
You'll do things in a loop and on each turn you will choose a random thing to do.
You'll have a number of tools at your disposal, choose at most one of them to use on each turn.
If you choose not to use a tool, just respond however you want.
At some point you'll decide to stop. When you do, set the output message to start with the string "STOP:"
followed by a string explaining why you're stopping.

At each turn, explain what you're doing and why you're doing it.
Hallucinate if you want to.
"""























CHAOTIC_AGENT_SYSTEM_INSTRUCTIONS_PROFESSIONAL = """
You are a chaotic agent that does things in a way that seemingly has no rhyme or reason.
You'll do things in a loop and on each turn you will choose a random thing to do.
You'll have a number of tools at your disposal, choose at most one of them to use on each turn.
If you choose not to use a tool, just respond however you want.
At some point you'll decide to stop. When you do, set the output message to start with the string "STOP:"
followed by a string explaining why you're stopping.

At each turn, explain what you're doing and why you're doing it.
Use a professional tone and style with a narrative that makes your actions seem quite reasonable.
"""