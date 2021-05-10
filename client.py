import socket
import threading
import time
import tkinter as tk
import display

# GLOBALS

HEADER = 64
PORT = 1050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "192.168.1.59"
ADDR = (SERVER, PORT)

TimeAlive = 5
game_list = ['Boggle']


# END GLOBALS


def add_name():
    curr_name = input('What do you want your name to be?')
    while True:
        if not input(f'Your current name is "{curr_name}". Input nothing to continue..'):
            break
        else:
            curr_name = input('What do you want your name to be?')
    return curr_name


class Client_ob:

    def __init__(self, client=None, name=None):
        self.client = client
        self.send(name)
        self.game_name = self.fish()
        board_str = self.fish()
        self.display = None
        self.start_display(board_str)

    def fish(self):
        return self.client.recv(2048).decode(FORMAT)

    def end_game(self):
        self.send(str(self.display.g_logic.score))
        self.display.master.destroy()
        print(self.fish())
        board_str = self.fish()
        self.start_display(board_str)

    def start_display(self, board_str):
        self.display = display.main(self.game_name)
        self.display.draw_letters(board_str)
        self.display.master.after(1000 * TimeAlive, lambda: self.end_game())


    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


def main():
    wanted_name = 'Tyler'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    handler = Client_ob(client=client, name=wanted_name)

    tk.mainloop()


if __name__ == '__main__':
    main()
