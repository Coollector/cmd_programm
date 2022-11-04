from app import command


from commands.binhexdec_command import main as binhexdec

command_list = [
    command(
        [
            "binhexdec",
            "This is a command to convert binary hexa decimal and decimal numbers",
            "nur eine schnelle help function",
        ],
        [
            ["binhex", "schnell", "schnell"],
            ["bindec", "schnell", "schnell"],
            ["decbin", "schnell", "schnell"],
            ["dechex", "schnell", "schnell"],
            ["hexbin", "schnell", "schnell"],
            ["hexdec", "schnell", "schnell"],
        ],
        binhexdec.main(),
        True,
    )
]


host = "162.55.212.105"

offline_check_tuple = ("8.8.8.8", 53)

app_name = "CLI - easy comands"
app_description = "\nThis is the easy Command Line Interface app"
prefix = "/"


# here are the commands, created with initialize.py


from commands.rechner import main as calc

command_list.append(
    command(
        [
            "calc",
            "calculator for all float calculations",
            "{prefix}calc {your calculations come here}",
        ],
        [],
        calc.main(),
        True,
    )
)


from commands.find_x import main as findX

command_list.append(
    command(
        ["findX", "Solves equation with one variable", "{prefix}findX {your equation}"],
        [],
        findX.main(),
        True,
    )
)


# from commands.suchfeld_solver import main as searchForWord

# command_list.append(command(['searchForWord', 'Initializes a path or userinput and searches for given words', '{prefix}searchForWord path {path to image} {words, sepererated by a comma: ','}'], [['getImage', 'Initializes a image to search for words in it', 'getImage {path to your image}'], ['inputByHand', 'Intitializes every character by hand', 'inputByHand {all characters inputed by Hand}'], ['findWord', 'finds the given word or words in the first initialized field (from image or from Hand)', "findWord {your word or words (seperated by a comma: ',')}"], ["correct", "you can correct the existing fields", "correct {(row, column, character)}"], ["print", "prints the existing field", "print"]], searchForWord.main(), False))
