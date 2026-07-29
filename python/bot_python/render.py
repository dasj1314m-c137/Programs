import flet as ft
import ask
import write_files
import asyncio
# ============================================================================
# VARIABLES GLOBALES PARA ALMACENAR REFERENCIAS DE FLET
# ============================================================================
# Estos almacenarán referencias a los componentes gráficos para que las
# funciones de UI puedan acceder a ellos sin pasar parámetros constantemente.

_page = None
_output_widget = None
_responsive = None
_audio_recorder = None
_audio_data_base = None

# ============================================================================
# FUNCIÓN DE INICIALIZACIÓN (LLÁMALA DESDE bot.py)
# ============================================================================
def init_render(page: ft.Page, output_widget: ft.Column, responsive=None):
    global _page, _output_widget, _responsive
    _page = page
    _output_widget = output_widget
    _responsive = responsive

def set_audio_deps(recorder, data_base):
    global _audio_recorder, _audio_data_base
    _audio_recorder = recorder
    _audio_data_base = data_base

# ============================================================================
# FUNCIÓN: smooth_print → ESCRIBE EN LA GUI
# ============================================================================
def smooth_print(txt: str, get_msj=False):
    # """
    # Reemplaza al antiguo print() de terminal.
    # Ahora agrega texto animado al widget de salida en la GUI.

    # El efecto de "escritura lenta" (smooth) se mantiene pero se ejecuta
    # carácter por carácter en el widget Flet.

    # Args:
    #     txt: El texto a mostrar
    # """
    # Si no se inicializó render, imprime en terminal (fallback para debugging)
    if _output_widget is None:
        print(f"[FALLBACK] {txt}")
        return

    # Crear un Card con estilo para que el mensaje tenga un fondo bonito
    # Fondo gris para contraste con el fondo negro, texto verde hacker

    # hacemos esta reasignacion para activar el __str__ de la clase y se pase como texto ya que en este caso no se activa porque es flet
    txt = str(txt)

    message_card = ft.Card(
        content=ft.Container(
            content=ft.Text(
                value=txt,
                size=14,
                color=ft.Colors.GREEN_ACCENT,
                selectable=True
            ),
            padding=12,
            bgcolor=ft.Colors.BLACK,  # Gris oscuro para contraste
            border_radius=5
        ),
        margin=8
    )

    # Agregamos el Card al contenedor
    _output_widget.controls.append(message_card)
    _page.update()

    if get_msj:
        return message_card

# ============================================================================
# FUNCIÓN: show_match → MUESTRA RESULTADOS EN LA GUI
# ============================================================================
async def show_match(matches, path):
    # """
    # Muestra los resultados de búsqueda/coincidencias en la GUI.

    # Si no hay coincidencias, ofrece agregar una nueva respuesta.
    # Si hay coincidencias, las muestra en un Card o Container destacado.

    # Esta función es ASYNC porque puede necesitar mostrar diálogos para
    # agregar nuevas respuestas. Úsala con 'await' en manager.py

    # Args:
    #     matches: El texto de coincidencias (string) o None
    #     path: La ruta del archivo donde se encontraron las coincidencias
    # """
    if not matches:
        # Sin coincidencias: mostrar mensaje y opción para agregar
        smooth_print("No hay coincidencias")
        # Preguntar al usuario si desea agregar otra respuesta
        add_response = await ask.questionSN("¿Quieres añadir otra posible respuesta?")
        if add_response:
            # Solicitar la nueva etiqueta
            new_pattern = await smooth_chat_input("Escribe la nueva etiqueta: ")
            # Si el usuario no canceló, solicitar la respuesta
            if new_pattern:
                new_response = await smooth_chat_input("Escribe la nueva respuesta: ")
                # Si el usuario no canceló, guardar en el archivo
                if new_response:
                    write_files.add_response(path, new_pattern, new_response)
                    smooth_print("✓ Respuesta agregada exitosamente")

    else:
        # Hay coincidencias: mostrar resultado en un Card destacado
        # Crear un contenedor visual atractivo para el resultado
        # Fondo gris con texto verde tipo hacker
        result_card = ft.Card(
            content=ft.Container(
                content=ft.Text(
                    value=matches,
                    size=13,
                    color=ft.Colors.GREEN_ACCENT,
                    selectable=True  # Permite al usuario copiar el texto
                ),
                padding=15,
                bgcolor=ft.Colors.BLACK,  # Fondo gris para contraste con fondo negro
                border_radius=5
            ),
            margin=10
        )

        # Agregar el Card al widget de salida
        if _output_widget is not None:
            _output_widget.controls.append(result_card)
            _page.update()
        else:
            smooth_print(matches)

# ============================================================================
# FUNCIÓN: smooth_chat_input → INPUT INTEGRADO EN LA CAJA NEGRA
# ============================================================================
async def smooth_chat_input(prompt: str, spell=False, skipable=False):
    # """
    # Crea un campo de entrada integrado en la ventana principal (no un diálogo).

    # El campo de texto y botón de envío aparecen como un Row al final del contenido,
    # permitiendo una experiencia tipo chat moderna. Después de que el usuario envía,
    # el mensaje aparece en el historial y el campo desaparece.

    # Soporta tanto Enter como clic en el botón de envío.

    # Esta función es ASYNC. Úsala con 'await'.

    # Args:
    #     prompt: El texto/pregunta a mostrar antes del campo de entrada
    #     spell: Si True y hay grabador disponible, añade botón de dictado

    # Returns:
    #     str: El texto ingresado por el usuario, o None si cancela
    # """
    if _page is None or _output_widget is None:
        print(f"[ERROR] render no inicializado. Pregunta: {prompt}")
        return None

    # Primero, mostrar la pregunta como un mensaje normal
    smooth_print(prompt)

    max_lines = _responsive.get_input_max_lines() if _responsive else 7

    input_field = ft.TextField(
        autofocus=True,
        multiline=True,
        expand=True,
        shift_enter=True,
        cursor_color=ft.Colors.GREEN_ACCENT,
        color=ft.Colors.GREEN_ACCENT,
        bgcolor=ft.Colors.BLACK,
        filled=True,
        border_color=ft.Colors.GREEN_ACCENT,
        max_lines=max_lines
    )

    # Crear el botón de envío con icono
    send_button = ft.IconButton(
        icon=ft.Icons.SEND,
        icon_size=24,
        tooltip="Enviar"
    )

    # Row que agrupa el TextField y el botón
    input_row = ft.Row(
        controls=[input_field, send_button],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER
    )

    if spell and _audio_recorder and _audio_data_base:
        is_transcribing = False

        async def on_dictation_click(e):
            nonlocal is_transcribing
            if is_transcribing:
                return
            await _audio_recorder.record_audio()
            if _audio_recorder.terminate:
                is_transcribing = True
                path = _audio_data_base.get_audio_path()
                if path:
                    msj_transcribe = smooth_print("Transcribiendo...", True)
                    _page.update()
                    import audio_processor as ap
                    transcribed = await ap.transcribe_audio(path, 'es')
                    input_field.value += transcribed if transcribed else ""
                    start_msj, end_msj = _audio_recorder.get_msjs()
                    _output_widget.controls.remove(start_msj)
                    _output_widget.controls.remove(end_msj)
                    _output_widget.controls.remove(msj_transcribe)
                    try:
                        import os
                        os.remove(path)
                    except Exception:
                        pass
                    _page.update()
                is_transcribing = False

        dictation_btn = _audio_recorder.make_button(on_dictation_click)
        input_row.controls.insert(-1, dictation_btn)

    cancelled = False

    # Variable para capturar el resultado
    result_value = None

    # Evento para sincronización asincrónica
    dialog_closed = asyncio.Event()

    # Contenedor vertical para el input y botón de cancelar
    input_container = ft.Column(
        controls=[input_row],
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    if skipable:

        def on_cancel(e):
            nonlocal cancelled
            cancelled = True
            try:
                _output_widget.controls.remove(input_container)
            except ValueError:
                pass
            _page.update()
            dialog_closed.set()

        cancel_button = ft.ElevatedButton(
            content=ft.Text("Cancelar"),
            on_click=on_cancel,
            style=ft.ButtonStyle(
                color=ft.Colors.GREEN_ACCENT,
                bgcolor=ft.Colors.BLACK
            )
        )
        input_container.controls.append(cancel_button)

    # Función que se ejecuta al enviar (botón o Enter)
    def on_send(e):
        nonlocal result_value
        text = input_field.value.strip()

        # Si el campo está vacío, no hacer nada
        if not text:
            return

        # Guardar el resultado
        result_value = text

        # Mostrar el mensaje del usuario en el historial como un card estático
        user_message_card = ft.Card(
            content=ft.Container(
                content=ft.Text(
                    value=text,
                    size=14,
                    color=ft.Colors.BLUE_ACCENT,  # Azul para diferenciar del bot
                    selectable=True
                ),
                padding=12,
                bgcolor=ft.Colors.GREY_900,  # Gris más oscuro
                border_radius=5
            ),
            margin=8
        )

        # Remover el input_container del widget de salida
        try:
            _output_widget.controls.remove(input_container)
        except ValueError:
            pass  # Ya fue removido o no existe

        # Agregar el mensaje del usuario al historial
        _output_widget.controls.append(user_message_card)

        # Actualizar la página
        _page.update()

        # Activar el evento para que se continúe con la ejecución
        dialog_closed.set()

    # Vincular el evento de envío al botón
    send_button.on_click = on_send

    # Vincular el evento Enter en el TextField
    input_field.on_submit = on_send

    # Agregar el input_container al widget de salida
    _output_widget.controls.append(input_container)
    _page.update()

    # Esperar a que el usuario envíe el mensaje
    await dialog_closed.wait()

    return False if cancelled else (result_value if result_value else None)

# ============================================================================
# FUNCIÓN: smooth_chat_buttons → INPUT CON BOTONES INTEGRADOS
# ============================================================================
async def smooth_chat_buttons(prompt: str, buttons: list):
    # """
    # Crea una pregunta con botones integrados en la ventana principal (no un diálogo).

    # Los botones aparecen como un Row al final del contenido, permitiendo una
    # experiencia tipo chat moderna. Después de que el usuario hace clic, el botón
    # y la pregunta permanecen en el historial.

    # Args:
    #     prompt: El texto/pregunta a mostrar
    #     buttons: Lista de tuplas (label, value) para los botones
    #             Ejemplo: [("Sí", True), ("No", False)]

    # Returns:
    #     El value del botón presionado, o None si se cancela
    # """
    if _page is None or _output_widget is None:
        print(f"[ERROR] render no inicializado. Pregunta: {prompt}")
        return None

    # Primero, mostrar la pregunta como un mensaje normal
    smooth_print(prompt)

    # Crear los botones
    button_controls = []
    result_value = None
    dialog_closed = asyncio.Event()

    def create_button_handler(btn_value):
        def on_button_click(e):
            nonlocal result_value
            result_value = btn_value
            result_label = e.control.content.value  # Obtener el texto del botón presionado

            # Remover el button_row del widget de salida
            try:
                _output_widget.controls.remove(button_row)
            except ValueError:
                pass

            # Mostrar el botón presionado como un card estático
            user_choice_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(
                        value=f"→ {result_label}",  # Flecha para indicar elección del usuario
                        size=14,
                        color=ft.Colors.BLUE_ACCENT,
                        selectable=False
                    ),
                    padding=12,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=5
                ),
                margin=8
            )

            # Agregar la elección al historial
            _output_widget.controls.append(user_choice_card)
            _page.update()

            # Activar el evento
            dialog_closed.set()

        return on_button_click

    # Crear los controles de botones
    for btn_label, btn_value in buttons:
        btn = ft.ElevatedButton(
            content=ft.Text(btn_label),
            on_click=create_button_handler(btn_value),
            style=ft.ButtonStyle(
                color=ft.Colors.GREEN_ACCENT,
                bgcolor=ft.Colors.BLACK
            )
        )
        button_controls.append(btn)

    # Row que agrupa los botones
    button_row = ft.Row(
        controls=button_controls,
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Agregar el button_row al widget de salida
    _output_widget.controls.append(button_row)
    _page.update()

    # Esperar a que el usuario haga clic
    await dialog_closed.wait()

    return result_value
