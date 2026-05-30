import json
import render
from datetime import datetime, timedelta

# ============================================================================
# FUNCIÓN: format_date_readable → CONVIERTE DATETIME A FORMATO LEGIBLE
# ============================================================================
def format_date_readable(fecha_obj):
    # """
    # Convierte un objeto datetime a formato legible: dia-dd-mes-yyyy

    # Ejemplo: lunes-29-mayo-2026

    # Args:
    #     fecha_obj (datetime): Objeto datetime a convertir

    # Returns:
    #     str: Fecha en formato legible, o None si no es válido
    # """
    if not isinstance(fecha_obj, datetime):
        return None

    # Mapeo de días de semana en español
    dias_nombre = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    # Mapeo de meses en español
    meses_nombre = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    # Obtener componentes
    dia_semana = dias_nombre[fecha_obj.weekday()]
    dia = fecha_obj.day
    mes = meses_nombre[fecha_obj.month - 1]
    año = fecha_obj.year

    # Retornar en formato legible
    return f"{dia_semana}-{dia:02d}-{mes}-{año}"

# ============================================================================
# FUNCIÓN: calculate_date → TRADUCE TEXTO A FECHA LEGIBLE
# ============================================================================
def calculate_date(texto):
    # """
    # Convierte descripciones naturales de fechas a formato legible.

    # Soporta:
    # - "hoy" → fecha actual
    # - "mañana" → fecha actual + 1 día
    # - Días de semana ("lunes", "martes", ..., "domingo") → próximo día

    # Args:
    #     texto (str): Descripción natural de la fecha

    # Returns:
    #     str: Fecha en formato legible (ej: lunes-29-mayo-2026), o None si no es reconocida
    # """
    if not isinstance(texto, str):
        return None

    # Normalizar entrada: minúsculas y sin espacios extra
    texto = texto.strip().lower()

    today = datetime.now()

    # Caso 1: "hoy"
    if texto == "hoy":
        return format_date_readable(today)

    # Caso 2: "mañana"
    if texto == "mañana":
        tomorrow = today + timedelta(days=1)
        return format_date_readable(tomorrow)

    # Caso 3: Días de la semana
    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "miercoles": 2,  # Alternativa sin tilde
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "sabado": 5,    # Alternativa sin tilde
        "domingo": 6
    }

    if texto in dias_semana:
        dia_objetivo = dias_semana[texto]
        dia_actual = today.weekday()

        # Calcular días para el próximo día de la semana
        dias_adelante = (dia_objetivo - dia_actual) % 7

        # Si es 0, significa que es hoy -> vamos al próximo de la semana siguiente
        if dias_adelante == 0:
            dias_adelante = 7

        fecha_objetivo = today + timedelta(days=dias_adelante)
        return format_date_readable(fecha_objetivo)

    # Si no coincide con ningún patrón, retorna None
    return None

def dic_index(dic, index):
    for i, key in enumerate(dic.items()):
        if i == index:
            return key

def list_view(list_content):
    for i, item in enumerate(list_content, 1):
        render.smooth_print(f"{i}. {item}")
    return None

def save_json_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def linkHeading_md(md_name, heading_name):
    return f"[[{md_name}#{heading_name}]]"

if __name__ == "__main__":
    list_test = ["item1", "item2", "item3"]
    list_view(list_test)