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

class Options:
    def __init__(self):
        self.name = []
        self.description = []
        self.date = []
        self.filtered_options = {}

    def get_attribute(self, attribute):
        if attribute == "name":
            return self.name
        elif attribute == "description":
            return self.description
        elif attribute == "date":
            return self.date
        else:
            raise ValueError("Invalid attribute for sorting")

    def set_atribute(self, attribute, value):
        if attribute == "name":
            len_attribute = len(self.name)
            self.name.append({"mark":len_attribute, "value":value})
        elif attribute == "description":
            len_attribute = len(self.description)
            self.description.append({"mark":len_attribute, "value":value})
        elif attribute == "date":
            len_attribute = len(self.date)
            self.date.append({"mark":len_attribute, "value":value})
        else:
            raise ValueError("Invalid attribute for sorting")

    def sort_attribute(self, attribute):
        if attribute == "name":
            attribute_sorted = sorted(self.name, key=lambda x: x["value"])
            return attribute_sorted
        elif attribute == "description":
            attribute_sorted = sorted(self.description, key=lambda x: x["value"])
            return attribute_sorted
        elif attribute == "date":
            attribute_sorted = sorted(self.date, key=lambda x: x["value"])
            return attribute_sorted
        else:
            raise ValueError("Invalid attribute for sorting")

    def sort_by(self, attribute_sorted, attribute_to_sort):
        new_attribute_sorted = []
        list_marks = [dic["mark"] for dic in attribute_sorted]
        for mark in list_marks:
            for dic_to_sort in attribute_to_sort:
                if mark == dic_to_sort["mark"]:
                    new_attribute_sorted.append(dic_to_sort)
        # forma de eliminar los valores mark por el momento si en algun momento los necesitamos
        # solo eliminamos la siguiente linea y en la funcion sort_join_by aplicar la limpieza
        new_attribute_sorted = [dic["value"] for dic in new_attribute_sorted]
        return new_attribute_sorted

    def join_attributes(self, attributes):
        options = []
        name = attributes[0]
        description = attributes[1] if attributes[1] else ""
        date = attributes[2] if attributes[2] else ""
        for i in range(len(attributes[0])):
            options.append(f"{name[i]} - {description[i]} {date[i]}")
        return options

    def sort_join_by(self, attribute, attribute_sorted):
        if self.name:
            name_attribute = self.sort_by(attribute_sorted, self.name) if not attribute == "name" else False
        if self.description:
            description_attribute = self.sort_by(attribute_sorted, self.description) if not attribute == "description" else False
        if self.date:
            date_attribute = self.sort_by(attribute_sorted, self.date) if not attribute == "date" else False
        # obtenemos solo los valores evitando la mark
        attribute_sorted = [dic["value"] for dic in attribute_sorted]
        if not name_attribute:
            attributes = [attribute_sorted, description_attribute, date_attribute]
            return self.join_attributes(attributes)
        elif not description_attribute:
            attributes = [name_attribute, attribute_sorted, date_attribute]
            return self.join_attributes(attributes)

    def get_by_mark(self, list_options):
        marks = [dic["mark"] for dic in list_options]
        descriptions_to_show = []
        dates_to_show = []
        for mark in marks:
            for dic in self.description:
                if mark == dic["mark"]:
                    dic = {"mark": mark, "value": dic["value"]}
                    descriptions_to_show.append(dic)
            for dic in self.date:
                if mark == dic["mark"]:
                    dic = {"mark": mark, "value": dic["value"]}
                    dates_to_show.append(dic)
        return [descriptions_to_show, dates_to_show]

    def procces_filter(self):
        options_show = [opt for opt in self.name if self.filtered_options.get(opt["value"]) != "ignore"]
        return options_show

class Messages:
    def __init__(self):
        self.select_msj = "Selecciona una opción:"

    def set_select_msj(self, msj):
        self.select_msj = msj
    def init_select_msj(self):
        self.select_msj = "Selecciona una opción:"
    def get_select_msj(self):
        return self.select_msj