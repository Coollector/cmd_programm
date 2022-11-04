from rich import print

if __name__ == "__main__":
    import user
    from app import app
    import settings

    import getpass
    import argparse
    import os
    import socket

    import inquirer
    from rich.traceback import install

    install(show_locals=True)

    languages = [
        str(elem).replace(".py", "")
        for elem in os.listdir(
            os.path.dirname(os.path.abspath(__file__)) + "\languages"
        )
    ]

    if not languages:
        if not os.path.exists("languages"):
            os.makedirs("languages")
        with open(f"{os.getcwd()}\languages\english.py", "w") as f:
            f.write(
                "username_taken = 'Username is already taken, please take a other one'\nusername_or_password_incorrect = 'Your username or password were incorrect. Please try again'\noffline_no_access = 'You can not acces the database in offline mode. Please relogin without offline tag'\n\n\nquit_description = 'quits the programm'\nquit_help = 'write {prefix}quit to stop the programm and safely close the console'\n\nhelp_description = 'shows this list'\nhelp_help = 'write {prefix}help {command} to see help about a specific command'\n\navaiable_commands = 'Avaiable commands'\n\nmain_menu_string = 'Main menu (help for menu)'\n\nbye = 'Bey'\n\noffline_packages = 'Tried to import not offline package'\n\ncommand_not_found = 'Command was not found, please try again'\n\nerror = 'something went wrong, please try again'"
            )
            f.close()

    parser = argparse.ArgumentParser(description="CLI - custom command - programm")
    parser.add_argument(
        "-u", "--user", help="logs in with the given username", required=True
    )
    parser.add_argument(
        "-n",
        "--newUser",
        help="creates new user in database",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--offline",
        help="activates offline mode. will only execute packages which don't need wifi",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Uses the given language from the languagepack",
        choices=languages,
        required=True,
    )

    args = parser.parse_args()

    if not args.offline:
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                settings.offline_check_tuple
            )
        except socket.error as e:
            print(
                "[italic yellow]Do you want to activate offline mode?[/]\n[bold red]Can not establish internet connection...[/]"
            )
            if inquirer.prompt([inquirer.Confirm("offline")])["offline"]:
                print("[bold green]OFFLINE MODE activated[/]")
                args.offline = True

    user = user.user(
        args.user,
        (None if args.offline else getpass.getpass("Please enter your password:")),
        (True if args.newUser else False),
        (True if args.offline else False),
        ("english" if args.language is None else args.language),
    )

    app = app(settings.app_name, settings.app_description, user, settings.prefix)
    for command in settings.command_list:
        app.register_command(command)

    app.run()

else:
    print("this is meant to be ran as main, please don't import it")
    quit()
