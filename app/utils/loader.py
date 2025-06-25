import os
import importlib
from flask import Blueprint

def load_blueprints_from_folder(app, folder):
    folder_path = folder.replace("/", ".")
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{folder_path}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
            except Exception as import_error:
                print(f"❌ Failed to import {module_name}: {import_error}")
                continue

            for attr in dir(module):
                obj = getattr(module, attr)
                # Only register if it is a Flask Blueprint instance
                if isinstance(obj, Blueprint):
                    try:
                        app.register_blueprint(obj, url_prefix="/api")
                        print(f"🔗 Registered blueprint: {obj.name}")
                    except Exception as e:
                        print(f"❌ Failed to register blueprint {obj.name}: {e}")
