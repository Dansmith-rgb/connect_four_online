import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.97"
port = 5555

#server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: Board(6, 7)}

spectartor_ids = []
specs = 0


def read_specs():
    global spectartor_ids

    spectartor_ids = []
    try:
        with open("specs.txt", "r") as f:
            for line in f:
                spectartor_ids.append(line.strip())
    except:
        print("[ERROR] No specs.txt file found, creating one...")
        open("specs.txt", "w")


def threaded_client(conn, game, spec=False):
    global pos, games, currentId, specs, connections

    if not spec:
        name = None
        bo = games[game]
        print(connections)
        connections += 1
        if connections % 2 == 0:
            currentId = "y"
        else:
            currentId = "r"

        bo.start_user = currentId

        # Pickle the object and send it to the server
        data_string = pickle.dumps(bo)

        if currentId == "y":
            bo.ready = True

        conn.send(data_string)
        #connections += 1
        print(connections)
        while True:
            if game not in games:
                break

            try:
                d = conn.recv(8192 * 3)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    if data.count("select") > 0:
                        all = data.split(" ")
                        col = int(all[1])
                        row = int(all[2])
                        color = all[3]
                        bo.drop_piece(col, row, color)
                        print("yeah")

                    if data == "winner b":
                        bo.winner = "b"
                        print("[GAME] Player b won in game", game)
                    if data == "winner w":
                        bo.winner = "w"
                        print("[GAME] Player w won in game", game)

                    if data.count("name") == 1:

                        name = data.split(" ")[1]

                        if currentId == "y":
                            bo.p2Name = name
                        elif currentId == "r":
                            bo.p1Name = name

                    sendData = pickle.dumps(bo)
                    #print("Sending board to player", currentId, "in game", game)

                conn.sendall(sendData)

            except Exception as e:
                print(e)

        connections -= 1
        try:
            del games[game]
            print("[GAME] Game", game, "ended")
        except:
            pass
        print("[DISCONNECT] Player", name, "left game", game)
        conn.close()


while True:
    if connections < 6:
        conn, addr = s.accept()
        spec = False
        g = -1
        print("[CONNECT] New connection")

        for game in games.keys():
            if games[game].ready == False:
                g = game

        if g == -1:
            try:
                g = list(games.keys())[-1] + 1
                games[g] = Board(6, 7)
            except:
                g = 0
                games[g] = Board(6, 7)

        print("[DATA] Number of Connections:", connections + 1)
        print("[DATA] Number of Games:", len(games))

        start_new_thread(threaded_client, (conn, g, spec))
