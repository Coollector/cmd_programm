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


from commands.suchfeld_solver import main as searchForWord

command_list.append(command(['searchForWord', 'Initializes a path or userinput and searches for given words', "{prefix}searchForWord path {path to image} {words, sepererated by a comma: ','}"], [], searchForWord.main(), False))


from commands.latin import main as latin

command_list.append(command(["latin", "translates everything from latin and gives you detailed information about the translation", "{prefix}latin {latin word}"], [], latin.main(), False))