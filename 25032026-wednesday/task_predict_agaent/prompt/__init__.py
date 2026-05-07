import os

BASE_PATH = os.path.dirname(__file__)

def load_prompt(name: str):
    file_path = os.path.join(BASE_PATH, f"{name}.md")
    with open(file_path, "r") as file:
        return file.read()