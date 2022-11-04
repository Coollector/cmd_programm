import inquirer
from rich import print
from rich.traceback import install

install(show_locals=True)


class _command:
    def __init__(self, command: str, description: str, command_help: str):
        self.command = command
        self.description = description
        self.command_help = command_help

    def __str__(self) -> str:
        return self.command + "\t\t" + self.description

    def __repr__(self) -> str:
        return self.command + "\t\t" + self.command_help


class command:
    """
    A class to initialize commands
    It handles the input and runs the application

    ...

    Attributes
    ----------
    main_command : list
        a list of length 3
            command without prefix
            description of the command
            help for the command
    sub_commands : list
        a list of lists
            only strings
            subcommand
            description
            help
                subcommands
    """

    def __init__(self, main_command: list, sub_commands: list, function, offline: bool):
        """
        Parameters
        ----------
        main_command : list
            a list of length 3
                command without prefix
                description of the command
                help for the command
        sub_commands : list
            a list of lists
                only strings
                subcommand
                description
                help
        function : function
            name of start function in your main.py
            structure:
                interface:/
                    app.py
                    __init__.py
                commands:/
                    custom_command:/
                        main.py
                            class main()
                                def run():      That is the function which gets called on entereing the command

                        utils:/
                            something.py
                        __init__.py
                    custom_command2:/
                        main.py
                            class main()
                                def run():      That is the function which gets called on entereing the command

                        whatever you want here
                        __init__.py
                main.py
                user.py
                config.json
                __init__.py
        """
        self.main_command = _command(main_command[0], main_command[1], main_command[2])
        self.sub_commands = []
        for command in sub_commands:
            self.sub_commands.append(_command(command[0], command[1], command[2]))
        self.command_function = function
        self.offline = offline

    def __str__(self) -> str:
        return (
            str(self.main_command)
            + "\n\t"
            + "\n\t".join([str(elem) for elem in self.sub_commands])
        )

    def run(self, app, command: str):
        call_length = len(app.prefix) + len(self.main_command.command) + 1
        try:
            self.command_function.run(app, self, command[call_length:])
        except Exception as e:
            print(e)
        return

    def __repr__(self):
        return (
            repr(self.main_command)
            + "\n\t"
            + "\n\t".join([repr(elem) for elem in self.sub_commands])
        )


class app:
    """
    A class to create a CLI interface
    with custom commands
    and password secured user management
    aswell as MySQL database access

    ...

    Attributes
    ----------
    name : str
        name of the application
        will be written at startup
    description : str
        description in main menu of your application
    user : user
        a user instance to store password and username
        access database trough this class
    prefix : str
        the prefix to be used to signal command using

    Methods
    -------
    register_command(command:command)
        adds a custom command to the app
        (will be displayed in the menu)

    run()
        starts the app with commands

    main_menu()
        goes back to the main menu and waits for the next user input

    restart()
        reloads all commands which have not been added

    quit()
        closes the application safely and signals to database

    menu()
        returns the string for the menu wiht all commands and subcommands
    """

    def __init__(self, name: str, description: str, user, prefix: str):
        self.name = name
        self.user = user
        self.description = description
        self.prefix = prefix
        self.sys_commands = [
            ["quit", self.user.language.quit_description, self.user.language.quit_help],
            ["help", self.user.language.help_description, self.user.language.help_help],
        ]
        self.commands = []
        self.commands_notadded = []
        self.running = False

    def run(self):
        print(
            f"""
██╗░░░██╗███████╗██████╗░░██████╗███████╗
██║░░░██║██╔════╝██╔══██╗██╔════╝██╔════╝
╚██╗░██╔╝█████╗░░██████╔╝╚█████╗░█████╗░░
░╚████╔╝░██╔══╝░░██╔══██╗░╚═══██╗██╔══╝░░
░░╚██╔╝░░███████╗██║░░██║██████╔╝███████╗
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚══════╝
─────────────────────────────────────────
"""
        )
        self.running = True
        print("\n\n\n-------------------------------------------------------------")
        print(self.name, end="\n\n")
        print(self.description)
        print("-------------------------------------------------------------\n\n\n")
        print(f"{self.user.language.avaiable_commands}:\n\n", end=" ")
        print(self.menu())
        self.main_menu()

    def main_menu(self):
        print(f"\n\n{self.user.language.main_menu_string}\n\n")
        user = input()
        self.execute(user)
        if not self.running:
            print(f"\n\n{self.user.language.bye} {self.user.username}\n")
            exit()
        self.main_menu()

    def register_command(self, command: command):
        if self.user.offline:
            if command.offline:
                if self.running:
                    self.commands_notadded.append(command)
                    return
                self.commands.append(command)
            else:
                print(
                    f"{self.user.language.offline_packages}: {command.main_command.command}"
                )
        else:
            if self.running:
                self.commands_notadded.append(command)
                return
            self.commands.append(command)
        return

    def restart(self):
        for i in self.commands_notadded:
            self.commands.append(i)
        self.commands_notadded = []

    def quit(self):
        self.running = False

    def menu(self):
        return (
            f"\n{self.prefix}"
            + f"\n{self.prefix}".join(
                [str(elem[0] + "\t" + elem[1]) for elem in self.sys_commands]
            )
            + f"\n\n{self.prefix}"
            + f"\n\n{self.prefix}".join([str(elem) for elem in self.commands])
            + "\n\n"
        )

    def help(self, command=None):
        if command == None:
            return (
                "\n\n"
                + f"\n{self.prefix}"
                + f"\n{self.prefix}".join(
                    [str(elem[0] + "\t" + elem[1]) for elem in self.sys_commands]
                )
                + f"\n\n\n{self.prefix}"
                + f"\n\n{self.prefix}".join([repr(elem) for elem in self.commands])
                + "\n\n"
            )
        else:
            for i in self.commands:
                if command == i.main_command.command:
                    return "\n\n" + repr(i)
            return self.user.language.command_not_found

    def execute(self, command: str):
        distributed = False
        for i in self.sys_commands:
            if command[1 : len(self.prefix) + 4] in i:
                if command[: len(self.prefix) + 4] == self.prefix + "help":
                    if len(command.replace(" ", "")) > 5:
                        print(self.help(command[6:]))
                    else:
                        print(self.help())
                    distributed = True
                elif command[: len(self.prefix) + 4] == self.prefix + "quit":
                    self.quit()
                    distributed = True
        if not distributed:
            possibilities = []
            for i in self.commands:
                command_name = i.main_command.command
                if (
                    self.prefix + command_name
                    == command[: len(command_name) + len(self.prefix)]
                ):
                    possibilities.append(i)
            if len(possibilities) == 1:
                possibilities[0].run(self, command)
                distributed = True
            elif len(possibilities) == 0:
                print(self.user.language.error)
                return
            else:
                command_choice = inquirer.prompt(
                    questions=[
                        inquirer.List(
                            "choice",
                            message="Because there are more then one commands with this name, please select the one you want:",
                            choices=[
                                f"{i+1} " + j.main_command.description
                                for i, j in enumerate(possibilities)
                            ],
                        ),
                    ]
                )
                possibilities[int(str(command_choice["choice"])[:1]) - 1].run()
        return
