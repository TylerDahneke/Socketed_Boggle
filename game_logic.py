import enchant
import tkinter as tk
import tkinter.font as font

# GLOBALS

BoggleDice = ['AAEEGN', 'ELRTTY', 'AOOTTW', 'ABBJOO',
              'EHRTVW', 'CIMOTU', 'DISTTY', 'EIOSST',
              'DELRVY', 'ACHOPS', 'HIMNQU', 'EEINSU',
              'EEGHNW', 'AFFKPS', 'HLNNRZ', 'DEILRX']

Padding = 20
BoxSize = 110
BackgroundBoxPosList = [[x, y] for y in range(Padding, 600, BoxSize + 2 * Padding)
                        for x in range(Padding, 600, BoxSize + 2 * Padding)]

FontSize = BoxSize - 2 * Padding


# END GLOBALS

def get_letter_pos(inp_pos, box_size, letter_padding=5):
    x, y = inp_pos
    dx = dy = (box_size - 2 * letter_padding) // 2
    return x + dx + letter_padding, y + dy + letter_padding


def get_index(x, y, wid):
    return y * wid + x


class Background_Square:

    def __init__(self, canvas, canvas_shape=None, pos=None, box_size=None, fill=None, funct=None, ob_type=None):
        if fill is None or fill == 'bg':
            self.fill = ['LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4']
        elif fill == 'green':
            self.fill = ['green2', 'green3', 'green4']
        elif fill == 'red':
            self.fill = ['firebrick2', 'firebrick3', 'firebrick4']
        self.canvas = canvas
        self.canvas_shape = canvas_shape

        self.letter = None
        self.letter_shape = None

        self.pos = pos
        self.box_size = box_size

        self.m_in = False
        self.selected = False

        self.funct = funct

        self.ob_type = ob_type

    def set_selected(self, override=None):
        if override:
            self.selected = False
        else:
            self.selected = not self.selected
        self.change_color()

    def set_m_out(self):
        self.m_in = False
        self.change_color()

    def set_m_in(self):
        self.m_in = True
        self.change_color()

    def assign_letter(self, shape, letter):
        self.letter_shape = shape
        self.letter = letter

    def change_color(self):
        if self.m_in is False and not self.selected:
            self.canvas.itemconfig(self.canvas_shape, fill=self.fill[0])
        elif self.m_in and not self.selected:
            self.canvas.itemconfig(self.canvas_shape, fill=self.fill[1])
        else:
            self.canvas.itemconfig(self.canvas_shape, fill=self.fill[2])


class BoggleLogic:

    def __init__(self, canvas=None):
        self.dice = BoggleDice
        self.canvas = canvas
        self.font = font.Font(family='Times New Roman', size=FontSize)
        self.m_pos = None
        self.background_squares = []
        self.menu_squares = []
        self.found_words = []
        self.last_square_ob_clicked = None
        self.dictionary = enchant.Dict('en_US')
        self.curr_str = ''
        self.score = 0

    def draw_letters(self, board_str):
        for square in self.background_squares:
            wanted_letter, board_str = board_str[0], board_str[1:]
            x, y = get_letter_pos(square.pos, BoxSize)
            text = self.canvas.create_text(x, y, text=wanted_letter,
                                           font=self.font)
            square.assign_letter(text, wanted_letter)

    def draw_board(self):
        for y_pos in range(Padding, 600, BoxSize + 2 * Padding):
            for x_pos in range(Padding, 600, BoxSize + 2 * Padding):
                curr = self.canvas.create_rectangle(x_pos, y_pos,
                                                    x_pos + BoxSize,
                                                    y_pos + BoxSize,
                                                    fill='LemonChiffon2')
                object_shape = Background_Square(self.canvas, canvas_shape=curr, pos=[x_pos, y_pos],
                                                 fill='bg', box_size=BoxSize,
                                                 ob_type='Background')
                self.background_squares.append(object_shape)

    def draw_menu(self):
        x, y = 600, 400
        curr = self.canvas.create_rectangle(x, y, 800 - Padding, 600 - Padding, fill='green2')
        try_shape = Background_Square(self.canvas, canvas_shape=curr, box_size=200 - Padding,
                                      pos=[x, y], fill='green',
                                      ob_type='Menu')
        self.menu_squares.append(try_shape)
        next = self.canvas.create_rectangle(x, y - 200, 800 - Padding, y - Padding, fill='firebrick2')
        clear_shape = Background_Square(self.canvas, canvas_shape=next, box_size=200 - Padding,
                                        pos=[x, y - 200], fill='red',
                                        ob_type='Menu')
        self.menu_squares.append(clear_shape)
        tx, ty = get_letter_pos((x, y - 400), 200 - Padding)
        final = self.canvas.create_text(tx, ty, text=self.score,
                                        font=self.font)
        score_shape = Background_Square(self.canvas, box_size=200 - Padding,
                                        pos=[x, y - 400],
                                        ob_type='Menu')
        score_shape.assign_letter(final, self.score)
        self.menu_squares.append(score_shape)

    def update_m_pos(self, pos):
        counter = 0
        self.m_pos = pos
        x, y = pos
        for square_object in self.background_squares:
            x2, y2 = square_object.pos
            if x2 < x < x2 + square_object.box_size and \
                    y2 < y < y2 + square_object.box_size:
                square_object.set_m_in()
            else:
                square_object.set_m_out()
            counter += 1

    def activate_funct_at_mouse(self):
        x, y = self.m_pos
        for square_objects in self.background_squares:
            x2, y2 = square_objects.pos
            if x2 < x < x2 + BoxSize and \
                    y2 < y < y2 + BoxSize:
                if not square_objects.selected:
                    if self.next_click_allowed(square_objects):
                        self.last_square_ob_clicked = square_objects
                        square_objects.set_selected()
                        self.add_to_str(square_objects.letter)
                    else:
                        print('It has to be closer to the last square')

        try_sq, cancel_sq, score_sq = self.menu_squares
        x2, y2 = try_sq.pos
        if x2 < x < x2 + try_sq.box_size and \
                y2 < y < y2 + try_sq.box_size:
            self.try_word()
            self.canvas.itemconfig(score_sq.letter_shape, text=self.score)
        x2, y2 = cancel_sq.pos
        if x2 < x < x2 + cancel_sq.box_size and \
                y2 < y < y2 + cancel_sq.box_size:
            self.clear_choice()

    def next_click_allowed(self, next_shape):
        if self.last_square_ob_clicked is None:
            self.last_square_ob_clicked = next_shape
            return True
        lx, ly = self.last_square_ob_clicked.pos
        nx, ny = next_shape.pos
        return (nx - 150 <= lx <= nx + 150) and \
               (ny - 150 <= ly <= ny + 150)

    def try_word(self):
        if self.curr_str != '':
            if self.dictionary.check(self.curr_str):
                if self.curr_str not in self.found_words:
                    print(f'Found! {self.curr_str}')
                    word_points = len(self.curr_str) - 1
                    self.found_words.append(self.curr_str)
                    self.score += word_points

                else:
                    print(f'{self.curr_str} already in!')
            else:
                print(f'{self.curr_str} is not a real word!')
        else:
            print(f'Why would you try to enter nothing?')

        self.clear_choice()

    def clear_choice(self):
        self.curr_str = ''
        self.last_square_ob_clicked = None
        self.reset_all_bg_squares()

    def add_to_str(self, letter):
        self.curr_str += letter

    def reset_all_bg_squares(self):
        self.curr_str = ''
        for bg_s in self.background_squares:
            bg_s.set_selected(override=True)


if __name__ == '__main__':
    logic = BoggleLogic()
    logic.draw_board()
