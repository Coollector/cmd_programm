class main():
	def __init__(self):
		self.app = None
		self.command = None
		self.running = False

	def run(self, app, command, user_input):
		self.app = app
		self.command = command
		self.types = ['translate']
		self.commands = self.types + ['help', 'menu', 'quit']

		# code for direct access goes here (user_input contains the whole entered line)

		self.running = True
		print('\n\n')
		print(self.menu())

		while self.running:
			print('\n\n')
			self.handle(input())

		return


	def help(self):
		return repr(self.command)

	def menu(self):
		return str(self.command)

	def quit(self):
		self.running = False

	def handle(self, user:str):
		user_input = user.split(' ')
		command = user_input[0]
		if command not in self.commands:
			print('Please enter a valid command')
			print(self.menu())
			return
		if command == 'help':
			print(self.help())
			return
		elif command == 'menu':
			print(self.menu())
			return
		elif command == 'quit':
			self.quit()
			return
		else:
			# here go your custom commands
			print('[italic red]Not yet implemented command[/]')
			return