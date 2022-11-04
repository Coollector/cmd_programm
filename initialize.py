from app import command

import os
import re
import time

import inspect
import importlib as implib
import argparse
import inquirer
from rich import print
from rich.traceback import install
install(show_locals=True)
from tqdm import tqdm


parser = argparse.ArgumentParser(description="Initializer for CLI - programm")
parser.add_argument(
    "-nl",
    "--newLanguage",
    help="creates a file in language directory to add a new language pack",
    required=False,
)
parser.add_argument(
    "-nCMD",
    "--newCommand",
    help="will bring up the command prompt to create a new command (can be done manually)",
    required=False,
    action="store_true",
)
parser.add_argument(
    "-db",
    "--database",
    help="Initialize a MySQL Database and add needed Columns",
    required=False,
    action="store_true",
)

args = parser.parse_args()
    
def create_settings():
    if not os.path.exists("settings.py"):
        print("[italic yellow]There is no settings.py file.\nDo you want to create it?[/]")
        create = inquirer.prompt([inquirer.confirm("create")])["create"]
        if create:
            with open(f"{os.getcwd()}\settings.py", "w") as f:
                f.write(
                    f"from app import command\n\ncommand_list = []\n\nhost = '162.55.212.105'\noffline_check_tuple = ('8.8.8.8', 53)\n\napp_name = 'Your apps name'\napp_description = 'Description for your app'\nprefix = '/'\t# prefix for your main commands"
                )

def new_language():
    if args.newLanguage is not None:
        if not os.path.exists("languages"):
            os.makedirs("languages")
        with open(f"{os.getcwd()}\languages\{args.newLanguage}.py", "w") as f:
            f.write(
                "username_taken = '' # Username is already taken, please take a other one\nusername_or_password_incorrect = '' # Your username or password were incorrect. Please try again\noffline_no_access = '' # You can not acces the database in offline mode. Please relogin without offline tag\nquit_description = '' # quits the programm\nquit_help = '' # write {prefix}quit to stop the programm and safely close the console\nhelp_description = '' # shows this list\nhelp_help = '' # write {prefix}help {command} to see help about a specific command\navaiable_commands = '' # Avaiable commands\nmain_menu_string = '' # Main menu (help for menu)\nbye = '' # Bey\noffline_packages = '' # Tried to import not offline package\ncommand_not_found = '' # Command was not found, please try again\nerror = '' # something went wrong, please try again"
            )


def new_command():
    if args.newCommand:
        if not os.path.exists("settings.py"):
            print("[bold red]You can not create a command without a settings.py file[/]")
            quit()

        command_direc_name = inquirer.prompt(
            [inquirer.Text("direc_name", "What do you want to name the command_directory")]
        )

        if os.path.exists(f"commands\{command_direc_name['direc_name']}"):
            while command_direc_name["direc_name"] in [
                str(elem).replace(".py", "")
                for elem in os.listdir(os.path.dirname(os.path.abspath(__file__)))
            ]:
                direc_name = input(
                    f"The folder name already exists in:\n{os.getcwd()}\commands\{command_direc_name['direc_name']}\nPlease either delete it now and press enter or enter a not existing directory name"
                )
                if not direc_name.replace(" ", "") == "":
                    command_direc_name["direc_name"] = direc_name

        print("\n\n")

        command_settings = inquirer.prompt(
            [
                inquirer.Text("command_name", "What do you want to call the main command"),
                inquirer.Text(
                    "command_description", "What should be the description for your command"
                ),
                inquirer.Text(
                    "command_help",
                    "When somebody needs help with your command, what should be printed",
                ),
            ]
        )

        print("Will the command be offline available")
        offline = inquirer.prompt([inquirer.Confirm("offline")])["offline"]

        subcommands_number = int(
            inquirer.prompt(
                [
                    inquirer.Text(
                        "subcommands_number",
                        "How many direct subcommand will there be",
                        validate=lambda _, x: re.match("^[-+]?[0-9]+$", x),
                    )
                ]
            )["subcommands_number"]
        )

        sub_commands = []

        for i in range(subcommands_number):
            sub_command_settings = inquirer.prompt(
                [
                    inquirer.Text(
                        "command_name", f"What do you want to call the {i+1}.  subcommand"
                    ),
                    inquirer.Text(
                        "command_description",
                        "What should be the description for the command",
                    ),
                    inquirer.Text(
                        "command_help",
                        "When somebody needs help with your command, what should be printed",
                    ),
                ]
            )
            sub_commands.append(list(sub_command_settings.values()))

        os.makedirs(f"commands\{command_direc_name['direc_name']}")

        # to make sure the file exists
        open(f"{os.getcwd()}\commands\\{command_direc_name['direc_name']}\__init__.py", "w")

        with open(
            f"{os.getcwd()}\commands\\{command_direc_name['direc_name']}\main.py", "w"
        ) as f:
            f.write(
                f"class main():\n\tdef __init__(self):\n\t\tself.app = None\n\t\tself.command = None\n\t\tself.running = False\n\n\tdef run(self, app, command, user_input):\n\t\tself.app = app\n\t\tself.command = command\n\t\tself.types = {str([str(elem[0]) for elem in sub_commands])}\n\t\tself.commands = self.types + ['help', 'menu', 'quit']\n\n\t\t# code for direct access goes here (user_input contains the whole entered line)\n\n\t\tself.running = True\n\t\tprint('\\n\\n')\n\t\tprint(self.menu())\n\n\t\twhile self.running:\n\t\t\tprint('\\n\\n')\n\t\t\tself.handle(input())\n\n\t\treturn\n\n\n\tdef help(self):\n\t\treturn repr(self.command)\n\n\tdef menu(self):\n\t\treturn str(self.command)\n\n\tdef quit(self):\n\t\tself.running = False\n\n\tdef handle(self, user:str):\n\t\tuser_input = user.split(' ')\n\t\tcommand = user_input[0]\n\t\tif command not in self.commands:\n\t\t\tprint('Please enter a valid command')\n\t\t\tprint(self.menu())\n\t\t\treturn\n\t\tif command == 'help':\n\t\t\tprint(self.help())\n\t\t\treturn\n\t\telif command == 'menu':\n\t\t\tprint(self.menu())\n\t\t\treturn\n\t\telif command == 'quit':\n\t\t\tself.quit()\n\t\t\treturn\n\t\telse:\n\t\t\t# here go your custom commands\n\t\t\tprint('[italic red]Not yet implemented command[/]')\n\t\t\treturn"
            )

        import_lib_object = implib.import_module("settings")
        existing_variables = [i[0] for i in inspect.getmembers(import_lib_object)]

        import_name = command_settings["command_name"]
        x = 1
        while import_name in existing_variables:
            import_name = "command" + str(x)
            x += 1

        with open(f"{os.getcwd()}\settings.py", "r+") as f:
            data = f.read()
            if "# here are the commands, created with initialize.py" not in data:
                f.write("\n\n\n# here are the commands, created with initialize.py")
            neue_zeile = "\n\t"
            f.write(
                f"\n\n\nfrom commands.{command_direc_name['direc_name']} import main as {import_name}\n\ncommand_list.append(\n\tcommand([\n\t'{command_settings['command_name']}',\n\t'{command_settings['command_description']}',\n\t'{command_settings['command_help']}'\n\t],\n\t{neue_zeile.join([str(sub_command) for sub_command in sub_commands])},\n\t{import_name}.main(), {str(offline)}))"
            )

def distributor(i):
    if i == 0:
        create_settings()
    elif i == 1 or i == 2:
        new_language()
    else:
        new_command()

for i in tqdm(range(10 if args.newCommand else 3)):
    time.sleep(2)
    distributor(i)

print("\n\n[bold green]Initialization succesfully finished[/]")
