import os
import importlib
import json

PLUGINS = {}

SAVE_FILE = os.path.join(os.path.dirname(__file__), "plugins.json")


# ---------------- LOAD ---------------- #
def load_plugins():
    print("\n[PLUGIN SYSTEM] Loading plugins...\n")

    PLUGINS.clear()

    base_path = os.path.dirname(__file__)

    for file in os.listdir(base_path):
        if file.endswith(".py") and file not in ["__init__.py", "loader.py"]:

            module_name = f"plugins.{file[:-3]}"

            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "run"):
                    PLUGINS[file[:-3]] = module.run
                    print(f"✔ Loaded: {file[:-3]}")

            except Exception as e:
                print(f"❌ Error: {file} -> {e}")

    save_plugins()


# ---------------- SAVE ---------------- #
def save_plugins():
    with open(SAVE_FILE, "w") as f:
        json.dump(list(PLUGINS.keys()), f)


# ---------------- LIST ---------------- #
def list_plugins():
    if not PLUGINS:
        print("\nNo plugins found.")
        return

    print("\nAvailable Plugins:")
    for i, name in enumerate(PLUGINS.keys(), 1):
        print(f"{i}. {name}")


# ---------------- RUN ---------------- #
def run_plugin(choice):
    try:
        name = list(PLUGINS.keys())[int(choice) - 1]
        print(f"\n[RUNNING] {name}\n")
        PLUGINS[name]()
    except:
        print("Invalid selection")


# ---------------- DELETE ---------------- #
def delete_plugin(name):
    path = os.path.join(os.path.dirname(__file__), f"{name}.py")

    if os.path.exists(path):
        os.remove(path)
        print(f"✔ Deleted plugin: {name}")
    else:
        print("Plugin not found")
