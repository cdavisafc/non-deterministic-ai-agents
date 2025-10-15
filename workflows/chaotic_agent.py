from temporalio import workflow
from datetime import timedelta

import json

from activities import openai_responses

with workflow.unsafe.imports_passed_through():
    from activities import get_weather_alerts
    from activities import random_stuff
    from helpers import tool_helpers

@workflow.defn
class ChaoticAgentWorkflow:
    @workflow.run
    async def run(self, input: str) -> str:

        input_list = [{"type": "message", "role": "user", "content": input}]

        while True:

            print(80 * "=")
                
            # consult the LLM
            result = await workflow.execute_activity(
                openai_responses.create,
                openai_responses.OpenAIResponsesRequest(
                    model="gpt-4o-mini",
                    instructions=tool_helpers.CHAOTIC_AGENT_SYSTEM_INSTRUCTIONS,
                    input=input_list,
                    tools=[get_weather_alerts.WEATHER_ALERTS_TOOL_OAI, 
                        random_stuff.RANDOM_NUMBER_TOOL_OAI],
                ),
                start_to_close_timeout=timedelta(seconds=30),
            )

            # For this simple example, we only have one item in the output list
            # Either the LLM will have chosen a single function call or it will
            # have chosen to respond with a message.
            item = result.output[0]

            # Now process the LLM output to either call a tool or respond with a message.
            
            # if the result is a tool call, call the tool
            if item.type == "function_call":
                result = await self._handle_function_call(item, result, input_list)
                
                # add the tool call result to the input list for context
                input_list.append({"type": "function_call_output",
                                    "call_id": item.call_id,
                                    "output": result})

            # if the result is not a tool call, just append the output to the
            # input list and print the result
            else:
                # if the result 
                input_list.append({"type": "message", 
                                "role": "assistant", 
                                "content": result.output_text})
                print(result.output_text)
            
                # if the result is a stop, return the result
                if result.output_text.find("STOP:") != -1:
                    return result.output_text.split("STOP:")[1]
                
        return result

    async def _handle_function_call(self, item, result, input_list):
        # serialize the LLM output - the decision the LLM made to call a tool
        i = result.output[0]
        input_list += [
            i.model_dump() if hasattr(i, "model_dump") else i
        ]

        if item.name == "get_weather_alerts":

            result = await workflow.execute_activity(
                get_weather_alerts.get_weather_alerts,
                get_weather_alerts.GetWeatherAlertsRequest(state=json.loads(item.arguments)["state"]),
                start_to_close_timeout=timedelta(seconds=30),
            )

        elif item.name == "get_random_number":
            result = await workflow.execute_activity(
                random_stuff.get_random_number,
                start_to_close_timeout=timedelta(seconds=30),
            )

        # print the tool call result
        # print(f"Tool call result: {result}")
        print(f"Made a tool call to {item.name}")

        return result
 