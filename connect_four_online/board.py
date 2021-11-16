import pygame
from constants import *


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.ready = False

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"

        self.turn = "y"

        self.winner = None

        self.ROW_COUNT = ROW_COUNT
        self.COL_COUNT = COL_COUNT
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.WIDTH = self.COL_COUNT * self.SQUARESIZE
        self.HEIGHT = (self.ROW_COUNT + 1) * self.SQUARESIZE

    def winning_move(self, piece):
        """
        Check for winning move

        :param piece: color of the counter
        :type piece: string
        """
        # Check horizontal locations for win
        for c in range(self.COL_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][
                        c + 1] == piece and self.board[r][
                            c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COL_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[
                        r + 1][c] == piece and self.board[
                            r + 2][c] == piece and self.board[r +
                                                              3][c] == piece:
                    return True

        # Check for positively sloped diaganols
        for c in range(self.COL_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][
                        c + 1] == piece and self.board[r + 2][
                            c + 2] == piece and self.board[r + 3][c +
                                                                  3] == piece:
                    return True

        # Check for negatively sloped diaganols
        for c in range(self.COL_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][
                        c + 1] == piece and self.board[r - 2][
                            c + 2] == piece and self.board[r - 3][c +
                                                                  3] == piece:
                    return True

    def draw_board(self, screen):
        """
        This function will draw the board and the counters in the board

        :param screen: what to draw on
        :type screen: object
        """
        for c in range(self.COL_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(
                    screen, BLUE,
                    (c * self.SQUARESIZE, r * self.SQUARESIZE +
                     self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(
                    screen, BLACK,
                    (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                     int(r * self.SQUARESIZE + self.SQUARESIZE +
                         self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COL_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == "r":
                    pygame.draw.circle(
                        screen, RED,
                        (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                         self.HEIGHT -
                         int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                        self.RADIUS)
                elif self.board[r][c] == "y":
                    pygame.draw.circle(
                        screen, YELLOW,
                        (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                         self.HEIGHT -
                         int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                        self.RADIUS)

    def drop_piece(self, row, col, color):
        """
        This function will update the row and column a 
        person wants a counter to be dropped

        :param row: which row to put counter in
        :type row: int
        :param col: which column to put counter in
        :type col: int
        :param color: The colour of the counter
        :type color: string
        """
        self.board[row][col] = color

    def is_valid_location(self, col):
        """
        Check if selected col is valid

        :param col: where to drop counter
        :type col: int
        """
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        """
        This function will get the next available 
        row which is available

        :param col: which column to place counter
        :type col: int
        """
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r
