import socket
from _thread import *
from board import Board
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.97"
port = 5555

# trying to set up socket to listen for incoming connectins.
try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

# Starting to listen for connectins.
s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: Board(6, 7)}

spectartor_ids = []
specs = 0


def read_specs():
    """
    Checks to see if specs.txt exists and creates a new one
    if there isn't one
    """
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
    """
    This is where the server recieves information about the game
    and relays to everyone in that game

    :param conn: allows the server to send and recieve data 
    on that connection
    :type conn: socket object
    :param game: Tells server what game somebody is in
    :type game: int
    :param spec: if true you are a spectator, defaults to False
    :type spec: bool, optional
    """
    global pos, games, currentId, specs, connections

    if not spec:
        name = None
        bo = games[game]

        if connections % 2 == 0:
            currentId = "y"

        else:
            currentId = "r"

        bo.start_user = currentId

        # Pickle the object and send it to the server
        data_string = pickle.dumps(bo)
        # If r(second player of the game) has joined then make the
        # game ready
        if currentId == "r":
            bo.ready = True
        conn.send(data_string)
        connections += 1

        # Start while loop
        while True:
            if game not in games:
                break

            try:
                # If server doesn't recieve any data break from loop
                d = conn.recv(8192 * 3)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    # If the data has select and space and all the
                    # other variables then it will go inside the if statement
                    if data.count("select") > 0:
                        # It splits up the data it has been sent
                        all = data.split(" ")
                        row = int(all[1])
                        col = int(all[2])
                        color = all[3]
                        # It calls a function which will drop a piece on the board
                        bo.drop_piece(row, col, color)
                        # It then changes who's turn it is
                        if bo.turn == "r":
                            bo.turn = "y"
                        else:
                            bo.turn = "r"

                    # If the data has winner y in it then set the board winner to y
                    if data == "winner y":
                        bo.winner = "y"
                        print("[GAME] Player y won in game", game)
                    # If the data has winner r in it then set the board winner to r
                    if data == "winner r":
                        bo.winner = "r"

                    # If data has name and somethinf after then check
                    # currentId and set players name
                    if data.count("name") == 1:

                        name = data.split(" ")[1]

                        if currentId == "y":
                            bo.p2Name = name
                        elif currentId == "r":
                            bo.p1Name = name

                    # Package all data up to send to players
                    sendData = pickle.dumps(bo)

                # Send all data to player
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
        # Close connection
        conn.close()


# Start loop to get game or create new game and call main function
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
