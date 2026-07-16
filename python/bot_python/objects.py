from datetime import datetime

class DataBase_Path:
    def __init__(self):
        # El método __init__ es el constructor. Se ejecuta al nacer el objeto.
        # Aquí preparamos la memoria. Al principio, no hay ruta. Obvio.
        self.folder_path = None
        self.file_path = None

    def save_dir_path(self, new_path):
        # Un método (acción) para guardar un dato en su memoria.
        self.folder_path = new_path

    def get_dir_path(self):
        # Otro método para extraer la información cuando la necesites.
        return self.folder_path

    def save_file_path(self, new_path):
        self.file_path = new_path

    def get_file_path(self):
        return self.file_path

class Messages:
    def __init__(self):
        self.select_msj = "Selecciona una opción:"

    def set_select_msj(self, msj):
        self.select_msj = msj
    def init_select_msj(self):
        self.select_msj = "Selecciona una opción:"
    def get_select_msj(self):
        return self.select_msj

class OptionsManager:
    def __init__(self):
        self.options = []
        self.filtered_options = []

    def add_due(self, due):
        self.options.append(due)

    def sort_dues(self):
        return sorted(self.options, key=lambda x: x.name)

    def clean_suffix(self, options):
        clean_options = []
        for opt in options:
            # El sufijo ".md" corresponde ahora a `description` (archivo).
            opt.description = opt.description.replace(".md", "")
            clean_options.append(opt)
        return clean_options

    def date_to_human(self):
        """
        Convierte las fechas de los pendientes a formato humanizado (ayer, hoy, mañana, día de semana)
        solo si están dentro de una semana. Las fechas fuera del rango mantienen human_date como None.

        Formato de entrada esperado: "lunes-07-julio-2026"
        """
        # Mapeos de meses en español
        meses_nombre = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
            "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }

        day_english = {
            "lunes": "Monday",
            "martes": "Tuesday",
            "miércoles": "Wednesday",
            "jueves": "Thursday",
            "viernes": "Friday",
            "sábado": "Saturday",
            "domingo": "Sunday"
        }

        today = datetime.now().date()

        for due in self.options:
            if due.date is None or due.human_date is not None:
                continue

            try:
                # Parsear la fecha en formato "lunes-07-julio-2026"
                partes = due.date.split("-")
                if len(partes) != 4:
                    continue

                dia_semana_str, dia_str, mes_str, año_str = [parte.strip() for parte in partes]

                # Convertir componentes
                dia = int(dia_str)
                año = int(año_str)

                # Normalizar mes (convertir nombre español a número)
                mes_str_lower = mes_str.lower()
                mes = meses_nombre.get(mes_str_lower)
                if mes is None:
                    continue

                # Crear objeto datetime
                fecha_due = datetime(año, mes, dia).date()

                # Calcular diferencia de días respecto a hoy
                diferencia = (fecha_due - today).days

                # Asignar human_date según la lógica
                # Si ya pasó por 2 o más días -> 'Pasado'
                if diferencia <= -2:
                    due.human_date = "Past"
                elif diferencia == -1:
                    due.human_date = "Yesterday"
                elif diferencia == 0:
                    due.human_date = "Today"
                elif diferencia == 1:
                    due.human_date = "Tomorrow"
                elif 2 <= diferencia <= 7:
                    # Está dentro de los próximos 7 días, extraer el día de semana del formato
                    # El primer componente ya es el día de semana
                    due.human_date = day_english[dia_semana_str.lower()]
                # Si diferencia > 7, mantener human_date como None

            except (ValueError, IndexError):
                # Si hay error en el parsing, dejar human_date como None
                continue

class Due:
    def __init__(self, name, description=None, date=None):
        self.name = name
        self.description = description
        self.date = date
        self.human_date = None

    def __str__(self):
        # Si human_date fue asignado, usarlo en lugar de date
        if self.human_date is not None:
                due = f"{self.name} - {self.human_date}"
        else:
            if self.date is not None:
                due = f"{self.name} - {self.date}"
            else:
                due = f"{self.name}"
        return due
