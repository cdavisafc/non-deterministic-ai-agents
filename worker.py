import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows.chaotic_agent import ChaoticAgentWorkflow
from activities import openai_responses, get_weather_alerts, random_stuff
from temporalio.contrib.pydantic import pydantic_data_converter


async def main():
    client = await Client.connect(
        "localhost:7233",
        data_converter=pydantic_data_converter,
    )

    worker = Worker(
        client,
        task_queue="chaotic-agent-python-task-queue",
        workflows=[
            ChaoticAgentWorkflow,
        ],
        activities=[
            openai_responses.create,
            get_weather_alerts.get_weather_alerts,
            random_stuff.get_random_number,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
