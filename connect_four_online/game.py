import numpy as np
import pygame
import sys
import math
from constants import *
from client import Network
import pickle

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#ROW_COUNT = 6
#COLUMN_COUNT = 7

#board = create_board()
#print_board(board)
#game_over = False
turn = 0

pygame.init()
pygame.font.init()


def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        #win.blit(chessbg, (0, 0))
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
    #win.blit(bo.board, (0, 0))
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
        if color == "w":
            txt3 = font.render("YOU ARE WHITE", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("YOU ARE BLACK", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("YOUR TURN", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 700))
        else:
            txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 700))

    pygame.display.update()


def end_screen(win, text):
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
                quit()
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT + 1:
                run = False


def connect():
    global n
    n = Network()
    return n.board


def main(win):

    global turn, bo, name
    game_over = False
    turn = 0

    color = bo.start_user
    print(color)

    count = 0

    #bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    pygame.display.update()
    #myfont = pygame.font.SysFont("monospace", 75)
    while game_over == False:
        try:
            ready = bo.ready
            redraw_gameWindow(win, bo, color, ready)
        except Exception as e:
            print("hi", e)
            end_screen(win, "Other player left")
            game_over = False
            break

        if not color == "s":
            if bo.winning_move("y"):
                bo = n.send("winner y")
            elif bo.winning_move("r"):
                bo = n.send("winner r")

        if bo.winner == "y":
            end_screen(win, "Yellow is the winner")
            game_over = False
        elif bo.winner == "r":
            end_screen(win, "Red is the winner")
            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.exit()
                exit()
                game_over = True

            if event.type == pygame.MOUSEMOTION:
                if color == bo.turn and bo.ready == True:
                    pygame.draw.rect(win, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if bo.turn == "r":
                        pygame.draw.circle(win, RED,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(win, YELLOW,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("yes")
                pygame.draw.rect(win, BLACK, (0, 0, WIDTH, SQUARESIZE))
                # print(event.pos)
                # Ask for player 1 input
                if bo.turn == "y":
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if bo.is_valid_location(col):
                        row = bo.get_next_open_row(col)
                        bo = n.send("select " + str(row) + " " + str(col) +
                                    " " +
                                    color)  #drop_piece(board, row, col, 1)

                        #if winning_move(board, 1):
                        #   print("Player 1 Wins!!!! Congrats!!!")
                        #   label = myfont.render("Player 1 Wins!", 1, RED)
                        #   self.SCREEN.blit(label, (40, 10))
                        #   game_over = True
                        #else:
                        #label = myfont.render("Players 2 go!", 2, RED)
                        #self.SCREEN.blit(label, (40, 10))

                # Ask for player 2 input

                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if bo.is_valid_location(col):
                        row = bo.get_next_open_row(col)
                        bo = n.send("select " + str(row) + " " + str(col) +
                                    " " +
                                    color)  #drop_piece(board, row, col, 2)

                        #if self.winning_move(board, 2):
                        #print("Player 2 Wins!!!! Congrats!!!")
                        #label = myfont.render("Player 2 Wins!", 1, YELLOW)
                        #screen.blit(label, (40, 10))
                        #game_over = True
                        #else:
                        #label = myfont.render("Players 1 go!", 2, YELLOW)
                        #screen.blit(label, (40, 10))

                #bo.draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    #pygame.time.wait(3000)
                    print("game_over")

    print(game_over)


name = input("Please type your name: ")
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Online")
menu_screen(win, name)
