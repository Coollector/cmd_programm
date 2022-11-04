import json
import socket
import mysql.connector
from mysql.connector import Error


def is_user(username, password):
    with open("users.json") as f:
        users = json.load(f)
    print(users)
    for i in users["users"]:
        print(i)
        if username in str(i):
            if i["password"] == password:
                return True
            else:
                return False
    return False


def create_user(username, password, connection):
    with open("users.json") as f:
        users = json.load(f)
        users["users"].append({"username": username, "password": password})
        json.dump(users, f)
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE {username} (test TEXT);")
    cursor.close


mysql = mysql.connector.connect(
    host="162.55.212.105", user="felix", passwd="fcfn061223", database="cmd_programm"
)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv.bind(("162.55.212.105", 8888))  # connect
serv.listen(5)  # wait for use
while True:
    connection, addr = serv.accept()
    result = ""
    while True:
        data = connection.recv(4096)
        if not data:
            break
        data = data.decode("utf-8")  # from binary to string
        print(data)
        data = data.split(" ")
        print(data)

        username = data[0]
        password = data[1]

        print(username)
        print(password)

        if data[2] == "create_user":
            create_user(username, password, mysql)
            result = "0 User created successfully"
            break

        if not is_user(username, password):
            result = "1 Password or username is wrong"
            break

        data = data[2:]
        data = " ".join([str(elem) for elem in data])

        if not data.lower().find("insert into " + username.lower()) or not (
            data.lower().find("select ")
            and data.lower().find(" from " + username.lower())
        ):
            result = f"2 can not access other tables then your own"
            break

        try:
            cursor = mysql.cursor()
            cursor.execute(data)
            result = "0" + " " + str(cursor.fetchall())
            cursor.close()
        except Error as e:
            result = "2" + " " + str(e)
        break

    connection.send(result.encode("utf-8"))
