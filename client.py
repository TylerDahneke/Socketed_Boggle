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


class Client_ob:

    def __init__(self, client=None):
        self.client = client
        game_name = self.fish()
        board_str = self.fish()
        self.display = display.main(game_name)
        self.display.draw_letters(board_str)

        self.display.master.after(1000 * TimeAlive, lambda: self.end_game())

    def fish(self):
        return self.client.recv(2048).decode(FORMAT)

    def end_game(self):
        self.send(str(self.display.g_logic.score))
        self.display.master.destroy()

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    handler = Client_ob(client=client)

    tk.mainloop()


def end_game(disp):
    send(str(disp.g_logic.score))
    disp.master.destroy()




def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


main()
