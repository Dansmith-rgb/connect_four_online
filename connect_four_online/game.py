import pygame
import sys
import math
from constants import *
from client import Network

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
pygame.font.init()


def menu_screen(win):
    """
    This is the menu screen function.
    It will tell you if the server is on and off

    :param win: where to place text
    :type win: surface
    """
    global bo, chessbg
    run = True
    offline = False

    while run:
        small_font = pygame.font.SysFont("comicsans", 50)

        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1,
                                    (255, 0, 0))
            win.blit(off, (WIDTH / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main(win)
                    break
                except:
                    print("Server Offline")
                    offline = True


def redraw_gameWindow(win, bo, color, ready):
    """
    This function draws most of the writing on the screen

    :param win: what to write the text on
    :type win: surface
    :param bo: The board
    :type bo: object
    :param color: What color the user is
    :type color: string
    :param ready: This will be true or false depending on if everyone is ready
    :type ready: Boolean
    """
    # Calling draw board function
    bo.draw_board(win)

    font = pygame.font.SysFont("comicsans", 30)

    txt = font.render("Press q to Quit", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))

    if ready == False:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (WIDTH / 2 - txt.get_width() / 2, 300))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "r":
            txt3 = font.render("YOU ARE RED", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("YOU ARE YELLOW", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("YOUR TURN", 1, (255, 0, 0))
            win.blit(txt3, (600, 10))
        else:
            txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
            win.blit(txt3, (600, 10))

    pygame.display.update()


def end_screen(win, text):
    """
    end screen function

    :param win: where to place text
    :type win: surface
    :param text:  Text to display on screen
    :type text: string
    """
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text, 1, (255, 0, 0))
    win.blit(txt, (WIDTH / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT + 1:
                run = False


def connect():
    """
    connect to server function
    """
    global n
    n = Network()
    return n.board


def main(win):
    """
    This is the main function of the game, handles all the game loops

    :param win: where to display counter ect on the screen.
    :type win: surface
    """

    global turn, bo, name
    game_over = False

    color = bo.start_user

    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    pygame.display.update()

    # Game loop
    while game_over == False:
        bo = n.send("get")
        clock.tick(30)
        try:
            ready = bo.ready
            redraw_gameWindow(win, bo, color, ready)
        except Exception as e:
            print("hi", e)
            end_screen(win, "Other player left")
            game_over = False
            break

        # Check for winner
        if not color == "s":

            if bo.winning_move("y"):
                bo = n.send("winner y")
            elif bo.winning_move("r"):
                bo = n.send("winner r")

        # If winner display who won by calling function
        if bo.winner == "y":
            end_screen(win, "Yellow is the winner")
            game_over = False
        elif bo.winner == "r":
            end_screen(win, "Red is the winner")
            game_over = False

        # Pygame loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                # Draw counter at top of screen
                if bo.ready == True:
                    pygame.draw.rect(win, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if color == "r":
                        pygame.draw.circle(win, RED,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(win, YELLOW,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(win, BLACK, (0, 0, WIDTH, SQUARESIZE))
                # Ask for player input
                print(bo.turn)
                if color == bo.turn and bo.ready:

                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if bo.is_valid_location(col):
                        row = bo.get_next_open_row(col)
                        bo = n.send("select " + str(row) + " " + str(col) +
                                    " " + color)

    n.disconnect()


# Getting name of player, setting up screen and calling the main
# function to run the game.
name = input("Please type your name: ")
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Online")
menu_screen(win, name)
