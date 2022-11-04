from utils import create_credentials
import os
import io
import json

from google.cloud import vision_v1 as vision
import pandas as pd
from rich import print
from rich.traceback import install
install(show_locals=True)
import inquirer


class main():
    def __init__(self):
        self.app = None
        self.command = None
        self.running = False

    def run(self, app, command, user_input):
        user_input = str(user_input)
        self.app = app
        self.command = command
        self.commands = ['help', 'menu', 'quit']

        credentials = self.app.user.execute(
            f"SELECT google_credentials FROM {self.app.user.username}")
        self.credentials = [True, credentials[2:]] if credentials[:1] == "0" else create_credentials.create_credentials(self.app.user)

        if not self.credentials[0]:
            print("[bold red]Please use a valid google_credentials json file.[/]")
            return
        self.credentials = self.credentials[1]

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials

        client = vision.ImageAnnotatorClient()

        if not user_input.replace(" ", "") == "":
            user_input = user_input.split(" ")
            image = user_input[0]
            if not os.path.exists(user_input[0]):
                print("[bold red]Please read the help description:[/]")
                print(repr(self.command.main_command.command))
                return
            try:
                words = str(' '.join([elem.replace('"', "'") for elem in user_input.pop(0)])).replace(' ', '').split(',')
            except:
                print("[bold red]Error occured in extracting words. Please reffere to help of the command:[/]")
                print(repr(self.command.main_command.command))
                return
            if not len(words) > 0:
                print("[bold red]Please reffere to the help of the command:[/]")
                print(repr(self.command.main_command.command))
                return

            prettie_cords_printer(Suchsel(client, inquirer.prompt([inquirer.Text("lines", "How many vertical lines are in the word search?")])["lines"], image).searchforword(words))     
            
            return
        
        else:
            print("[bold red]This command is only for inline use[/]")
            return

        self.suchsel = None
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


class Suchsel():
    def __init__(self, client, lines, image_path):
        self.chars = gettext(image_path, lines, client)
        


    def getdirections(self, i, j, length):
        return_list = []
        if i < length:
            return_list.append(False)
        else:
            return_list.append(True)
        if len(self.chars) - i < length:
            return_list.append(False)
        else:
            return_list.append(True)
        if j < length:
            return_list.append(False)
        else:
            return_list.append(True)
        if len(self.chars[i]) - j < length:
            return_list.append(False)
        else:
            return_list.append(True)
        return return_list

    def getcords(self, i, j, word):
        finds = []
        richtung = self.getdirections(i, j, len(word))

        if richtung[0]:
            for k in range(len(word) - 1):
                if not self.chars[i-k-1][j] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i-len(word)+1, j+1]])
        if richtung[0] and richtung[3]:
            for k in range(len(word) - 1):
                if not self.chars[i-k-1][j+k+1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i-len(word)+1, j+len(word)]])
        if richtung[1] and richtung[3]:
            for k in range(len(word) - 1):
                if not self.chars[i+k+1][j+k+1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i+len(word), j+len(word)]])
        if richtung[1]:
            for k in range(len(word) - 1):
                if not self.chars[i+k+1][j] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i+len(word), j+1]])
        if richtung[3]:
            for k in range(len(word) - 1):
                if not self.chars[i][j+k+1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i+1, j+len(word)]])
        if richtung[1] and richtung[2]:
            for k in range(len(word) - 1):
                if not self.chars[i+k+1][j-k-1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i+len(word), j-len(word)+2]])
        if richtung[2]:
            for k in range(len(word) - 1):
                if not self.chars[i][j-k-1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i+1, j-len(word)+2]])
        if richtung[0] and richtung[2]:
            for k in range(len(word) - 1):
                if not self.chars[i-k-1][j-k-1] == word[k+1]:
                    break
                finds.append([word, [i+1, j+1], [i-len(word)+1, j-len(word)+2]])
        if finds == []:
            finds = [False, False]
        else:
            finds.append(True)
        return finds
    
    def searchforword(self, woerter:list):
        words = []
        for k in woerter:
            words.append(str(k).lower())
        ergebnis_list = []
        for i in range(len(self.chars)):
            for j, char in enumerate(self.chars[i]):
                for word in words:
                    if char == word[0]:
                        result = self.getcords(i, j, word)
                        if result[1]:
                            ergebnis_list.append(result[0])
                            words.remove(word)
        return ergebnis_list
    
    def __str__(self):
        return_string = ""
        for i in self.chars:
            return_string = return_string + " ".join(str(elem) for elem in i) + "\n"
        return return_string



def gettext(path, lines, client, filename = None):
    chars = []
    row = []
    path = os.path.join(path, filename) if filename is not None else path
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['locale', 'description'])
    for text in texts:
        df = df.append(
            dict(
                locale = text.locale,
                description = text.description
            ),
            ignore_index = True
        )

    ergebnis = str(df.to_dict()['description'][0]).lower().replace(' ', '').replace('\n', '')

    for i in range(lines):
        row = []
        divided = int(len(ergebnis) / lines)
        for j in range(divided):
            row.append(ergebnis[j+(divided*i)])
        chars.append(row)
    return chars

def prettie_cords_printer(cords_list:list):
    print('\n\n\n\n')
    for i in cords_list:
        for j in i:
            print(str(j)+" ", end='')
        print('\n')