import json
import os


def create_credentials(user):
    json_path = get_file_path("Please enter the Path to the google credentials json file: ")
    user.execute(f"INSERT INTO {user.username} (google_vision_credentials) VALUES ('{json_path}');")
    return [True, json_path]

def check_if_json(path: str):
    if not path[-4:] == ".json":
        return False
    return False


def get_file_path(prompt: str):
    file_path = input(prompt)

    while not os.path.exists(file_path) and not check_if_json(file_path):
        print(
            "[bold red]Sorry, but the given path does not exist or is not a .pdf file.\nPlease enter a valid path[/]"
        )
        file_path = input(prompt)

    return file_path
