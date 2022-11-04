from rich import print
from rich.traceback import install

install(show_locals=True)

import sympy
from sympy.abc import x

abc = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
numbs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class main:
    def __init__(self):
        self.app = None
        self.command = None
        self.running = False

    def run(self, app, command, user_input: str):
        self.app = app
        self.command = command

        if (
            not user_input.replace(" ", "")
            == self.app.prefix + self.command.main_command.command
        ):
            variable = ""
            for i in user_input.replace(" ", ""):
                if i in abc:
                    if variable != "":
                        if not i == variable:
                            print(
                                "[bold red]This command is just able to calculate with one variable[/]"
                            )
                            return
                    else:
                        variable = i

            if variable == "":
                print(
                    "[bold red]Please use a calculator for calculations without variables[/]"
                )
                return

            user_input = user_input.replace(" ", "").replace(variable, "x")
            if "=" in user_input:
                user_input = user_input.replace("=", "-(") + ")"

            formated_ergenis_list = []
            ergebnis_list = list(user_input)
            for i, char in enumerate(ergebnis_list):
                formated_ergenis_list.append(char)
                if char == variable:
                    if i != len(ergebnis_list) - 1 and (
                        ergebnis_list[i + 1] in numbs
                        or ergebnis_list[i + 1] == variable
                    ):
                        formated_ergenis_list.append("*")
                if char in numbs:
                    if i != len(ergebnis_list) - 1 and ergebnis_list[i + 1] == variable:
                        formated_ergenis_list.append("*")

            user_input = "".join([str(elem) for elem in formated_ergenis_list])

            try:
                ergebnis = sympy.solve(user_input, x)[0]
            except sympy.SympifyError as e:
                print(f"[bold red]{e}[/]")
                return

            calculated = ""
            for i in str(ergebnis):
                if not i in numbs:
                    try:
                        calculated = f" [bold green](=[/][italic yellow] {int(ergebnis)}[/] [bold green])[/]"
                    except:
                        pass
                    break

            print(
                f"""[bold green]{variable}[/] = [italic yellow]{ergebnis}[/]{calculated}"""
            )
            return
        else:
            print(
                f"[bold red]Please refer to help of the command:[/]\n\n[italic green]{repr(self.command.main_command.command_help)}[/]"
            )
            return
