class main():
    def __init__(self):
        self.app = None
        self.command = None
        self.running = False

    def run(self, app, command, user_input):
        """runs the commmand

        Args:
            app (app): the app which runs rn and contains all useful variables
            command (command): the command which got executed with all its helps and descriptions
            user_input (str): the string which got enter without the command call
        """
        self.app = app
        self.command = command
        self.types = ['translate']
        self.commands = self.types + ['help', 'menu', 'quit']
        

        
        return