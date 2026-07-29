import json
import os
from pathlib import Path
import render
import traceback
import write_files

def _get_app_storage_dir():
    if os.environ.get("BOT_DEV_MODE") == "1":
        return Path.cwd() / ".sandbox_data" / ".bot_python"
    flet_storage = os.environ.get("FLET_APP_STORAGE_DATA")
    if flet_storage:
        return Path(flet_storage)
    return Path.cwd() / ".local_data" / ".bot_python"

def _get_global_config_dir():
    return _get_app_storage_dir()

def _get_global_config_path():
    return _get_global_config_dir() / "config.json"


def _get_default_root():
    return _get_app_storage_dir() / "data"


def get_data_json_path():
    return _get_app_storage_dir() / "data.json"


def get_global_config():
    config_path = _get_global_config_path()
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return None


def save_global_config(root_path):
    try:
        config_dir = _get_global_config_dir()

        config_dir.mkdir(parents=True, exist_ok=True)

        with open(_get_global_config_path(), "w") as f:
            json.dump({"root_path": str(root_path)}, f, indent=4)

    except Exception:
        render.smooth_print(traceback.format_exc())
        raise


def ensure_structure(root_path):
    dirs = ["diary", "dues", "book_learnings", "audios"]
    for d in dirs:
        path = Path(root_path, d)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            render.smooth_print(f"No se pudo crear {path}")
            print("ERROR:", repr(e))

    dues_md = Path(root_path, "dues", "dues.md")
    if not dues_md.exists():
        write_files.wadd_file(dues_md, "")

    init_root_data_json(root_path)


def init_root_data_json(root_path):
    storage_dir = _get_app_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    data_json_path = storage_dir / "data.json"
    if data_json_path.exists():
        return

    initial = {
        "metadata": {"last_update": "", "root_path": str(root_path)},
        "daily_status": {
            "mood_asked": False,
            "day_written": False,
            "dues_shown": False,
            "dues_modified": False
        },
        "times_asked": {
            "day_written": 0,
            "dues_shown": 0,
            "dues_modified": 0
        },
        "actions_paths": {
            "diary": "",
            "dues_file": str(Path(root_path, "dues", "dues.md")),
            "dues_dir": str(Path(root_path, "dues")),
            "books_dir": str(Path(root_path, "book_learnings"))
        }
    }
    with open(data_json_path, "w") as f:
        json.dump(initial, f, indent=4)


async def show_welcome_screen(page):
    import ask
    import search
    from objects import DataBase_Path, Messages

    msgs = Messages()
    msgs.set_select_msj("Elige cómo configurar tu almacenamiento:")
    choice = await ask.select_option(
        ["Usar carpeta predeterminada", "Elegir carpeta personalizada"],
        msgs
    )

    if choice is None:
        return None

    if choice == "Usar carpeta predeterminada":
        root = _get_default_root()
        save_global_config(root)
        try:
            ensure_structure(root)
            render.smooth_print("Creación de carpetas exitosa")
        except Exception:
            render.smooth_print(traceback.format_exc())
        return root

    if choice == "Elegir carpeta personalizada":
        data_base = DataBase_Path()
        await search.folder_picker(
            data_base,
            prompt="Selecciona la carpeta raíz para tus archivos"
        )
        root = data_base.get_dir_path()
        if root:
            save_global_config(root)
            try:
                ensure_structure(root)
                render.smooth_print("Creación de carpetas exitosa")
            except Exception:
                render.smooth_print(traceback.format_exc())
            return root

    return None
