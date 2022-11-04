class main:
    def __init__(self):
        self.app = None
        self.command = None
        self.running = False

    def run(self, app, command, user_input):
        self.app = app
        self.command = command

        if not user_input.replace(" ", "") == "":
            print(eval(user_input.replace(" ", "")))
            return
        else:
            print("[bold red]Please reffere to the help of the command:[/]")
            print(self.command.main_command.command_help)
