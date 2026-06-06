import asyncio
from pywhispercpp.model import Model
import ollama


# Transcribe audio file to text using pywhispercpp
# Comentarios en español, nombres de funciones y variables en inglés
async def transcribe_audio(audio_path: str) -> str:
    # """Transcribe el archivo WAV en `audio_path` usando pywhispercpp.

    # Devuelve el texto concatenado en inglés.
    # """
    def transcribe() -> str:
        model = Model("base")
        # La API de pywhispercpp devuelve una lista (o iterable) de segmentos con atributo .text
        result = model.transcribe(audio_path)
        try:
            texts = [segment.text for segment in result]
        except Exception:
            # Si no es iterable esperado, devolver la representación como fallback mínimo
            return str(result)
        return " ".join(t.strip() for t in texts if t)

    text = await asyncio.to_thread(transcribe)
    return text.strip()


# Send transcribed text to local Ollama Llama and return the reply
# Comentarios en español, nombres en inglés
async def talk_with_coach(messages):
    # """Enviar `user_text` a Ollama (modelo `llama3.2:3b`) y devolver la respuesta.

    # Usa un System Prompt estricto para comportarse como coach de inglés.
    # """

    def call_ollama() -> str:
        # Llamada directa a la API de Ollama
        response = ollama.chat(model="llama3.2:3b", messages=messages)
        # Extraer contenido principal según la estructura esperada
        try:
            return response["message"]["content"].strip()
        except Exception:
            # Fallback mínimo: intentar claves comunes
            if isinstance(response, dict) and "content" in response:
                return response["content"].strip()
            # Si no es el formato esperado, devolver la representación
            return str(response).strip()

    reply = await asyncio.to_thread(call_ollama)
    return reply

if __name__ == "__main__":
    async def test():
        txt = await transcribe_audio("test_limpio.wav")
        if txt:
            reply = await talk_with_coach(txt)
            print(reply)

    asyncio.run(test())