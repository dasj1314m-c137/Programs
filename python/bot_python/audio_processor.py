import asyncio
from pywhispercpp.model import Model
import ollama
import utils
import render
import flet as ft


# Transcribe audio file to text using pywhispercpp
# Comentarios en español, nombres de funciones y variables en inglés
async def transcribe_audio(audio_path: str, lang='en') -> str:
    # """Transcribe el archivo WAV en `audio_path` usando pywhispercpp.

    # Devuelve el texto concatenado en inglés.
    # """
    def transcribe() -> str:
        model = Model("base")
        # La API de pywhispercpp devuelve una lista (o iterable) de segmentos con atributo .text
        result = model.transcribe(audio_path, language=lang)
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


class AudioRecorder:
    def __init__(self, audio_recoder):
        self.audio_recorder = audio_recoder
        self.audio_buffer = bytearray()
        self.data_base = None
        self.audio_path = None

        self.func = None
        self.action = False
        self.terminate = False

        self.button = ft.IconButton(
            icon=ft.Icons.MIC,
            icon_color=ft.Colors.GREEN_ACCENT,
            bgcolor=ft.Colors.BLACK,
            on_click=None,
            data=False
        )
        self.msj_start = None
        self.msj_end = None

    async def func_to_use(self):
        await self.func(self.data_base)

    async def record_audio(self):
        if not self.button.data:
            self.terminate = False
            self.button.data = True
            self.button.icon = ft.Icons.STOP_CIRCLE
            self.button.icon_color = ft.Colors.RED
            self.button.update()

            self.audio_buffer.clear()
            self.msj_start = render.smooth_print("Iniciando grabacion..", True)
            stamp_path = utils.create_stamp_path("record", "wav")
            current_audio_path = f"audios/{stamp_path}"
            self.audio_path = current_audio_path
            self.data_base.save_audio_path(self.audio_path)
            await self.audio_recorder.start_recording(self.audio_path)

        else:
            try:
                self.button.data = False
                self.button.icon = ft.Icons.MIC
                self.button.icon_color = ft.Colors.GREEN_ACCENT
                self.button.update()

                if self.audio_path is None:
                    print("Sin path valiedo")
                    return

                self.msj_end = render.smooth_print("Grabacion terminada", True)
                await self.audio_recorder.stop_recording()

                raw_bytes = bytes(self.audio_buffer)
                self.audio_buffer.clear()

                if not raw_bytes:
                    print("sin entrada de audio")
                    return

                utils.save_pcm_to_wav(raw_bytes, self.audio_path)

                if self.action:
                    await self.func_to_use()

                self.terminate = True

            except FileNotFoundError as error_404:
                print(f"Error 404, {error_404}")
            except Exception as ex:
                print(f"🚨 lol: {ex}")

    def make_button(self, func=record_audio):
        self.button.on_click = func
        return self.button

    def get_msjs(self):
        return self.msj_start, self.msj_end

if __name__ == "__main__":
    # test whisper
    from pywhispercpp.model import Model

    model = Model("base")

    try:
        result = model.transcribe()
        print("El parámetro translate existe.")
    except TypeError as e:
        print(e)
