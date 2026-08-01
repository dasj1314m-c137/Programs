from fastapi import FastAPI, UploadFile, File, Form
import pywhispercpp.model as whisper
import asyncio
import os
from typing import Optional

app = FastAPI(title="Whisper API en Pi 5")

MODEL_DIR = "/app/models"
MODEL_NAME = "base"
COMUN_KEYWORDS = [
    # Hardware y Sistemas
    "Raspberry", "Mac", "Linux",
    # Lenguajes y Frameworks
    "Python", "Flet",
    # Herramientas y Librerías
    "pywhispercpp", "Ollama", "Docker", "Ngrok", "Obsidian",
    # Términos generales
    "IA", "bot", "API", "JSON", "SSH", ".py", ".json", ".toml", ".txt", "script",
    "venv", "_", "True", "False", "self", ".", "atributo", "url's", "url", "GitHub",
    "keys", "key", "API's"
]

initial_prompts = ",".join(COMUN_KEYWORDS)

model = whisper.Model(MODEL_NAME, models_dir=MODEL_DIR, n_threads=4)

@app.get("/")
def index():
    return {"status": "ok", "message": "Servidor de Whisper activo en la Pi 5"}

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form("en")
):
    temp_path = f"/tmp/{file.filename}"

    # Guardar el archivo recibido
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Función que corre la transcripción (síncrona)
    def run_transcription():
        return model.transcribe(temp_path, language=language, initial_prompt=initial_prompts)

    # Delegar la tarea pesada a un hilo secundario para no congelar la API
    results = await asyncio.to_thread(run_transcription)

    # Limpiar archivo temporal
    if os.path.exists(temp_path):
        os.remove(temp_path)

    txt_transcribed = "".join([segment.text for segment in results])

    return {"txt": txt_transcribed}
