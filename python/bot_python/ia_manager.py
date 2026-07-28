import asyncio
import ollama


async def talk_with_coach(messages):
    def call_ollama():
        response = ollama.chat(model="llama3.2:3b", messages=messages)
        try:
            return response["message"]["content"].strip()
        except Exception:
            if isinstance(response, dict) and "content" in response:
                return response["content"].strip()
            return str(response).strip()

    reply = await asyncio.to_thread(call_ollama)
    return reply
