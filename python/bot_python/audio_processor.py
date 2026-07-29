import asyncio
import requests
import utils
import render
import flet as ft
import os
from dotenv import load_dotenv

load_dotenv()

try:
    if not os.environ.get("TRANSCRIBE_PI5") == "1":
        from pywhispercpp.model import Model
        IS_WHISPER_LOCAL_AVAILABLE = True
    else:
        IS_WHISPER_LOCAL_AVAILABLE = False
except (ImportError, ModuleNotFoundError):
    IS_WHISPER_LOCAL_AVAILABLE = False

if IS_WHISPER_LOCAL_AVAILABLE:
    model = Model("base")
else:
    REMOTE_NGROK_URL = os.getenv("REMOTE_NGROK_URL")

async def connection_pi5():
    def check():
        try:
            resp = requests.get(url=f"{REMOTE_NGROK_URL}/", timeout=40)
            return resp.ok
        except requests.exceptions.RequestException as ex:
            render.smooth_print(f"Chequeo conexion pi-5 fail: {ex}")
            return False
    return await asyncio.to_thread(check)

async def transcribe_audio(audio_path: str, lang='en') -> str:
    if IS_WHISPER_LOCAL_AVAILABLE:
        def transcribe() -> str:
            result = model.transcribe(audio_path, language=lang)
            try:
                texts = [segment.text for segment in result]
            except Exception:
                return str(result)
            return " ".join(t.strip() for t in texts if t)

        text = await asyncio.to_thread(transcribe)
        return text.strip()
    else:
        def remote_transcribe() -> str:
            try:
                with open(audio_path, 'rb') as f:
                    files = {'file': f}
                    resp = requests.post(
                        f"{REMOTE_NGROK_URL}/transcribe",
                        files=files,
                        data={'language': lang},
                        timeout=40
                    )
                if resp.status_code == 200:
                    return resp.json().get('txt', '')
                return "Servicio de dictado por voz no disponible en este momento."
            except requests.exceptions.RequestException:
                return "Servicio de dictado por voz no disponible en este momento."

        return await asyncio.to_thread(remote_transcribe)

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
            if not IS_WHISPER_LOCAL_AVAILABLE and not await connection_pi5():
                render.smooth_print("Servicio de dictado por voz no disponible en este momento")
                return
            self.terminate = False
            self.button.data = True
            self.button.icon = ft.Icons.STOP_CIRCLE
            self.button.icon_color = ft.Colors.RED
            self.button.update()

            self.audio_buffer.clear()
            self.msj_start = render.smooth_print("Iniciando grabacion..", True)
            stamp_path = utils.create_stamp_path("record", "wav")
            root_path = self.data_base.get_root_path() if self.data_base else ""
            current_audio_path = f"{root_path}/audios/{stamp_path}"
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
                print(f"\U0001f6a8 lol: {ex}")

    def make_button(self, func=record_audio):
        self.button.on_click = func
        return self.button

    def get_msjs(self):
        return self.msj_start, self.msj_end
