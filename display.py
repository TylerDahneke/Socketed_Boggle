import tkinter as tk
import tkinter.font as font
import game_logic
import time

# import smart_list

# GLOBALS

GameBoardDimensions = {'Boggle': [800, 600]}


# ENDGLOBALS


def main(game_name):
    disp = create_display(game_name=game_name)
    disp.draw_board()
    disp.draw_menu()
    return disp


def create_display(game_name):
    root = tk.Tk()

    base = display(master=root, game_name=game_name)

    root.bind('<Motion>', lambda e: base.update_m_pos(e))
    root.bind('<Button-1>', lambda _: base.choose_square())
    root.bind('<KeyPress-c>', lambda _: base.check_word())

    return base

class display:

    def __init__(self, master=None, game_name=None):
        self.master = master
        board_width, board_height = GameBoardDimensions[game_name]
        self.canvas = tk.Canvas(master, width=board_width, height=board_height)

        self.g_logic = game_logic.BoggleLogic(self.canvas)

        self.canvas.pack()
        self.create_time = time.time()

    def draw_board(self):
        self.g_logic.draw_board()

    def draw_menu(self):
        self.g_logic.draw_menu()

    def draw_letters(self, board_str):
        self.g_logic.draw_letters(board_str)

    def update_m_pos(self, e):
        self.g_logic.update_m_pos((e.x, e.y))

    def choose_square(self):
        self.g_logic.activate_funct_at_mouse()

    def check_word(self):
        self.g_logic.try_word()


if __name__ == '__main__':
    main()
