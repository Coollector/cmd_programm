import importlib
import socket
import json
import datetime

from settings import host


class user:
    def __init__(
        self, username: str, password, new_user: bool, offline: bool, language
    ):
        self.username = username
        self.password = password
        language = importlib.import_module(f"languages.{language}")
        self.language = language
        self.login_time = datetime.datetime.now()
        self.offline = offline

        if not self.offline:
            executer = self.execute(f"SELECT settings FROM {username}")
            if executer[:1] == "0":
                if new_user:
                    print(self.language.username_taken)
                else:
                    self.settings = json.loads(executer[5:-4])
            else:
                if executer[:1] == "1":
                    if new_user:
                        print(self.execute("create_user")[2:])
                        self.settings = json.loads(
                            self.execute(f"SELECT settings FROM {username}")
                        )
                    else:
                        print(self.language.username_or_password_incorrect)
                else:
                    print(executer)

    def execute(self, query: str) -> str:
        """
        0 = good
        1 = password or username errors
        2 = mysql error
        """
        if self.offline:
            print(self.language.offline_no_access)
            quit()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, 8888))

        query = self.username + " " + self.password + " " + query

        sending = query.encode("utf-8")  # encode to bytes
        client.send(sending)  # send
        from_server = client.recv(4096)  # recieve answer
        from_server = from_server.decode("utf-8")
        client.close()

        return from_server
