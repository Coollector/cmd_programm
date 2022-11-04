import string


class main:
    def __init__(self):
        self.app = None
        self.command = None
        self.running = False

    def run(self, app, command, user_input):
        self.app = app
        self.command = command
        self.types = ["binhex", "bindec", "decbin", "dechex", "hexbin", "hexdec"]
        self.commands = self.types + ["help", "menu", "quit"]
        quit_after = True if user_input[-5:] == "-quit" else False
        user_input = user_input.replace(" ", "")
        if user_input != "":
            if quit_after:
                user_input = user_input[:-5]
            conversion_type = user_input[:3] + user_input[-3:]
            if conversion_type in self.types:
                zahl = user_input[3:-4]
                if not (
                    all(x in string.hexdigits for x in zahl)
                    if conversion_type == "hexbin" or conversion_type == "hexdec"
                    else zahl.isdigit()
                ):
                    print("Please enter a valid number to convert")
                    return
                exec(f"self.{conversion_type}('{zahl}')")
                if quit_after:
                    return
            else:
                print("Something went wrong with your input, please try again")
                return
        self.running = True
        print("\n\n")
        print(self.menu())
        while self.running:
            print("\n\n")
            self.handle(input())
        return

    def help(self):
        return repr(self.command)

    def menu(self):
        return str(self.command)

    def quit(self):
        self.running = False

    def handle(self, user: str):
        user_input = user.split(" ")
        command = user_input[0]
        if command not in self.commands:
            print("Please enter a valid command")
            print(self.menu())
            return
        if command == "help":
            print(self.help())
            return
        elif command == "menu":
            print(self.menu())
            return
        elif command == "quit":
            self.quit()
            return
        else:
            if not (
                all(x in string.hexdigits for x in user_input[1])
                if command == "hexbin" or command == "hexdec"
                else user_input[1].isdigit()
            ):
                print("Please enter a valid number to convert")
                return
            exec(f"self.{command}('{user_input[1]}')")

    def binhex(self, user: str):
        print(format(int(user, 2), "x"))

    def bindec(self, user: str):
        print(int(user, 2))

    def dechex(self, user: str):
        print(format(user, "x"))

    def decbin(self, user: str):
        print(bin(int(user)))

    def hexdec(self, user: str):
        print(int(user, 16))

    def hexbin(self, user: str):
        print(bin(int(user, 16)))
