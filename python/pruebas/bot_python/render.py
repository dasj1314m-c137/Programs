import flet as ft
import ask
import write_files
import asyncio

# ============================================================================
# VARIABLES GLOBALES PARA ALMACENAR REFERENCIAS DE FLET
# ============================================================================
# Estos almacenarán referencias a los componentes gráficos para que las
# funciones de UI puedan acceder a ellos sin pasar parámetros constantemente.

_page = None  # Referencia a la página principal de Flet
_output_widget = None  # Widget donde escribiremos los mensajes (ft.Column o ft.ListView)

# ============================================================================
# FUNCIÓN DE INICIALIZACIÓN (LLÁMALA DESDE bot.py)
# ============================================================================
def init_render(page: ft.Page, output_widget: ft.Column):
    # """
    # Inicializa las referencias globales de Flet.
    # DEBES LLAMAR A ESTO AL INICIO DE main() EN bot.py

    # Args:
    #     page: La página de Flet (ft.Page)
    #     output_widget: El widget donde mostrar mensajes (ft.Column o ft.ListView)
    # """
    global _page, _output_widget
    _page = page
    _output_widget = output_widget

# ============================================================================
# FUNCIÓN: smooth_print → ESCRIBE EN LA GUI
# ============================================================================
def smooth_print(txt: str):
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
async def smooth_chat_input(prompt: str):
    # """
    # Crea un campo de entrada integrado en la ventana principal (no un diálogo).

    # El campo de texto y botón de envío aparecen como un Row al final del contenido,
    # permitiendo una experiencia tipo chat moderna. Después de que el usuario envía,
    # el mensaje aparece en el historial y el campo desaparece.

    # Soporta tanto Enter como clic en el botón de envío.

    # Esta función es ASYNC. Úsala con 'await'.

    # Args:
    #     prompt: El texto/pregunta a mostrar antes del campo de entrada

    # Returns:
    #     str: El texto ingresado por el usuario, o None si cancela
    # """
    if _page is None or _output_widget is None:
        print(f"[ERROR] render no inicializado. Pregunta: {prompt}")
        return None

    # Primero, mostrar la pregunta como un mensaje normal
    smooth_print(prompt)

    # Crear el campo de entrada
    input_field = ft.TextField(
        label="Respuesta",
        autofocus=True,
        multiline=False,
        expand=True  # Se estira para ocupar el espacio disponible
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
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Variable para capturar el resultado
    result_value = None

    # Evento para sincronización asincrónica
    dialog_closed = asyncio.Event()

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

        # Remover el input_row del widget de salida
        try:
            _output_widget.controls.remove(input_row)
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

    # Agregar el input_row al widget de salida
    _output_widget.controls.append(input_row)
    _page.update()

    # Esperar a que el usuario envíe el mensaje
    await dialog_closed.wait()

    return result_value if result_value else None

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
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700
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
