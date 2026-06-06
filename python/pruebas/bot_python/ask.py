import render
import flet as ft
import asyncio
import utils
from datetime import datetime as dt

# ============================================================================
# ACCESO A LA PÁGINA DE FLET
# ============================================================================
# Funciones auxiliares para obtener la referencia a la página desde render
def _get_page():
    # """Retorna la página de Flet guardada en render"""
    return render._page

# ============================================================================
# FUNCIÓN: questionSN → PREGUNTA SÍ/NO INTEGRADA EN LA VENTANA
# ============================================================================
async def questionSN(question):
    # """
    # Realiza una pregunta Sí/No con botones integrados en la ventana.

    # Reemplaza la versión anterior que hacía un loop esperando "si" o "no".
    # Ahora usa botones gráficos integrados: [Sí] [No]

    # Esta función es ASYNC. Úsala con 'await' en manager.py:
    #     respuesta = await ask.questionSN("¿Deseas continuar? ")

    # Args:
    #     question: La pregunta a mostrar

    # Returns:
    #     bool: True si hace clic en "Sí", False si hace clic en "No"
    # """
    result = await render.smooth_chat_buttons(question, [("Sí", True), ("No", False)])
    return result if result is not None else False

# ============================================================================
# FUNCIÓN: open_question → PREGUNTA ABIERTA INTEGRADA EN LA VENTANA
# ============================================================================
async def open_question(question):
    # """
    # Realiza una pregunta abierta con un campo de entrada integrado en la ventana.

    # Esta función es ASYNC. Úsala con 'await' en manager.py:
    #     respuesta = await ask.open_question("¿Tu nombre? ")

    # Args:
    #     question: La pregunta a mostrar

    # Returns:
    #     str: El texto ingresado por el usuario, o None si cancela
    # """
    result = await render.smooth_chat_input(question)
    return result if result else None
# ============================================================================
# FUNCIÓN: select_option → SELECCIONA DE UNA LISTA EN DIÁLOGO
# ============================================================================
async def select_option(options, obj_message):
    # """
    # Permite al usuario seleccionar una opción de una lista.

    # Reemplaza la versión anterior que mostraba la lista en terminal.
    # Ahora usa un diálogo con RadioGroup o botones de selección.

    # Esta función es ASYNC. Úsala con 'await' en manager.py:
    #     opcion = await ask.select_option(["Opción 1", "Opción 2"])

    # Args:
    #     options: Lista de opciones para elegir
    #     ask_select: Si True, pregunta primero si desea seleccionar

    # Returns:
    #     int: El índice (0-based) de la opción seleccionada,
    #          False si cancela el ask_select inicial,
    #          None si cancela la selección
    # """

    page = _get_page()

    # Si no se inicializó render
    if page is None:
        print("[ERROR] Flet no inicializado.")
        return None

    # NUEVA LÓGICA: siempre mostramos un selector integrado en la ventana
    # El usuario puede seleccionar una opción y luego "Aceptar" o
    # simplemente no seleccionar nada y hacer "Aceptar" (devuelve None),
    # o "Cancelar" (también devuelve None).

    result_value = None
    dialog_closed = asyncio.Event()

    # Grupo de radio (valores como índices 0-based en string)
    radio_controls = [ft.Radio(
        value=str(i),
        label=opt,
        active_color=ft.Colors.GREEN_ACCENT,
        label_style=ft.TextStyle(bgcolor=ft.Colors.BLACK, color=ft.Colors.GREEN_ACCENT)
        )
        for i, opt in enumerate(options)
        ]

    # Contenedor que agrupa las opciones
    options_column = ft.Column(controls=radio_controls, spacing=6)

    # Inicializar RadioGroup con el contenido (requerido por Flet)
    radio_group = ft.RadioGroup(content=options_column)

    # Botones Aceptar / Cancelar
    def on_accept(e):
        nonlocal result_value
        if radio_group.value is not None:
            try:
                result_value = int(radio_group.value)
            except Exception:
                result_value = None
        else:
            result_value = None

        obj_message.init_select_msj()
        # Limpiar la interfaz: remover el bloque de selección
        try:
            _ = render._output_widget.controls.remove(selection_block)
        except Exception:
            pass

        # Mostrar la elección del usuario en el historial (si seleccionó algo)
        if result_value is not None:
            sel_label = options[result_value]
            user_choice_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(value=f"→ {sel_label}", size=14, color=ft.Colors.BLUE_ACCENT),
                    padding=12,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=5
                ),
                margin=8
            )
            render._output_widget.controls.append(user_choice_card)

        render._page.update()
        dialog_closed.set()

    def on_cancel(e):
        nonlocal result_value
        result_value = None
        obj_message.init_select_msj()
        try:
            _ = render._output_widget.controls.remove(selection_block)
        except Exception:
            pass
        render._page.update()
        dialog_closed.set()

    msj_title = ft.Text(
        value=obj_message.get_select_msj(),
        size=16,
        color=ft.Colors.GREEN_ACCENT
    )

    accept_btn = ft.ElevatedButton(
        content=ft.Text("Aceptar"),
        on_click=on_accept,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLACK, color=ft.Colors.GREEN_ACCENT)
        )
    cancel_btn = ft.ElevatedButton(
        content=ft.Text("Cancelar"),
        on_click=on_cancel,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLACK, color=ft.Colors.GREEN_ACCENT)
        )

    actions_row = ft.Row(controls=[accept_btn, cancel_btn], spacing=8, alignment=ft.MainAxisAlignment.CENTER)

    # Bloque que contiene opciones y acciones (para remover de una vez)
    selection_block = ft.Card(
        content=ft.Container(
            content=ft.Column(controls=[msj_title, radio_group, actions_row], spacing=10),
            padding=10,
            bgcolor=ft.Colors.BLACK,
            border_radius=5
        ),
        margin=8
    )

    # Agregar controles al output
    render._output_widget.controls.append(selection_block)
    render._page.update()

    # Esperar interacción
    await dialog_closed.wait()

    return result_value

# ============================================================================
# FUNCIÓN: ask_date_hybrid → ENTRADA DE FECHA TECLADO + CALENDARIO
# ============================================================================
async def ask_date_hybrid(question):
    # """
    # Permite al usuario ingresar una fecha de forma híbrida:
    # - Teclado: Escribir "hoy", "mañana", "lunes", etc.
    # - Ratón: Presionar botón "Calendario" para selector visual

    # Esta función es ASYNC. Úsala con 'await' en manager.py:
    #     fecha = await ask.ask_date_hybrid("¿Para cuándo es el pendiente? ")

    # Args:
    #     question: La pregunta a mostrar

    # Returns:
    #     str: Fecha en formato YYYY-MM-DD, o None si cancela
    # """
    page = _get_page()

    if page is None:
        print(f"[ERROR] Flet no inicializado. Pregunta: {question}")
        return None

    # Mostrar la pregunta
    render.smooth_print(question)

    # Variable para capturar resultado y evento de sincronización
    result_date = None
    dialog_closed = asyncio.Event()

    # Botón Aceptar - procesa el texto ingresado (se define ANTES de usarse)
    def on_accept_date(e):
        nonlocal result_date
        text = date_input.value.strip()

        # Intentar convertir el texto natural a fecha
        calculated_date = utils.calculate_date(text)

        if calculated_date is None:
            # Permitir reintentar: limpiar el campo
            date_input.value = ""
            page.update()
            return

        # Fecha válida encontrada
        result_date = calculated_date

        # Remover el bloque de entrada
        try:
            render._output_widget.controls.remove(date_input_block)
        except Exception:
            pass

        # Mostrar la fecha seleccionada en el historial
        date_card = ft.Card(
            content=ft.Container(
                content=ft.Text(
                    value=f"📅 {result_date}",
                    size=14,
                    color=ft.Colors.BLUE_ACCENT
                ),
                padding=12,
                bgcolor=ft.Colors.GREY_900,
                border_radius=5
            ),
            margin=8
        )
        render._output_widget.controls.append(date_card)
        render._page.update()

        # Liberar el semáforo
        dialog_closed.set()

    # Crear el campo de entrada para texto natural
    date_input = ft.TextField(
        label="Ingresa la fecha p.ej: hoy, mañana, lunes...",
        color=ft.Colors.GREEN_ACCENT,
        bgcolor=ft.Colors.BLACK,
        border_color=ft.Colors.GREEN_ACCENT,
        label_style=ft.TextStyle(color=ft.Colors.GREEN_ACCENT),
        hint_style=ft.TextStyle(color=ft.Colors.GREEN_ACCENT),
        autofocus=True,
        multiline=False,
        expand=True,
        hint_text="hoy, mañana, lunes, etc.",
        on_submit=on_accept_date  # Permitir enviar con Enter
    )

    # Botón Calendario - abre DatePicker
    today = dt.now()
    date_picker = ft.DatePicker(
        first_date=dt(year=today.year, month=today.month, day=today.day),
        last_date=dt(year=today.year + 2, month=12, day=31)
    )
    page.overlay.append(date_picker)

    def on_calendar_click(e):
        # Abrir el DatePicker
        page.show_dialog(date_picker)

    def on_date_selected(e):
        nonlocal result_date
        if date_picker.value:
            # Convertir la fecha seleccionada a formato legible
            result_date = utils.format_date_readable(date_picker.value)

            # Remover el bloque de entrada
            try:
                render._output_widget.controls.remove(date_input_block)
            except Exception:
                pass

            # Mostrar la fecha seleccionada en el historial
            date_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(
                        value=f"📅 {result_date}",
                        size=14,
                        color=ft.Colors.BLUE_ACCENT
                    ),
                    padding=12,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=5
                ),
                margin=8
            )
            render._output_widget.controls.append(date_card)
            render._page.update()

            # Liberar el semáforo
            dialog_closed.set()

    # Vincular el manejador de cambio al DatePicker
    date_picker.on_change = on_date_selected

    accept_btn = ft.ElevatedButton(
        content=ft.Text("Aceptar"),
        on_click=on_accept_date,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700)
    )

    calendar_btn = ft.IconButton(
        icon=ft.Icons.CALENDAR_TODAY,
        icon_size=24,
        tooltip="Calendario",
        on_click=on_calendar_click
    )

    # Row de botones
    buttons_row = ft.Row(
        controls=[accept_btn, calendar_btn],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Bloque que agrupa input + botones
    date_input_block = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[date_input, buttons_row],
                spacing=10
            ),
            padding=10,
            width=480,
            bgcolor=ft.Colors.BLACK,
            border_radius=5
        ),
        margin=8
    )

    # Agregar al output
    render._output_widget.controls.append(date_input_block)
    render._page.update()

    # Esperar a que el usuario seleccione una fecha válida
    await dialog_closed.wait()

    return result_date if result_date else None
