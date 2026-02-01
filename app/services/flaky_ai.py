# app/services/flaky_ai.py
import asyncio
import random

class FlakyAIUnavailable(Exception):
    pass

async def flaky_ai_process(call_id: str) -> dict:
    await asyncio.sleep(random.uniform(1, 3))
    if random.random() < 0.25:
        raise FlakyAIUnavailable("Flaky AI unavailable")

    return {
        "transcript": f"Transcript for call {call_id}",
        "sentiment": random.choice(["positive", "neutral", "negative"])
    }
