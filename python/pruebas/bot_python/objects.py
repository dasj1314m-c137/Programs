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
            opt.name = opt.name.replace(".md", "")
            clean_options.append(opt)
        return clean_options

class Due:
    def __init__(self, name, description=None, date=None):
        self.name = name
        self.description = description
        self.date = date

    def __str__(self):
        if self.date is not None and self.description is not None:
            due = f"{self.name} - {self.description} - {self.date}"
        else:
            due = f"{self.name}"
        return due
