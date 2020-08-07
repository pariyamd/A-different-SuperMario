from tkinter import *
import numpy as np

size_of_board = 600
Green_color = '#7BC043'


class Board():
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.window = Tk()
        self.window.title('Mushroom Eater!')
        self.w = int(size_of_board / max(self.m, self.n))
        self.canvas = Canvas(self.window, width=self.w * self.m+100, height=self.w * self.n)
        self.canvas.pack()
        self.initialize_board()

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(self.m):
            self.canvas.create_line((i + 1) * self.w, 0, self.w * (i + 1), self.w*self.n)
        for i in range(self.n):
            self.canvas.create_line(0, (i + 1) * self.w, self.w*self.m, (i + 1) * self.w)
        for x, y in {1: 3, 5: 2}.items():
            self.canvas.create_rectangle(self.w * x, self.w * y, self.w * (x + 1), self.w * (y + 1), outline="#000",
                                         fill="#000")
        for x, y in {2: 3, 5: 3}.items():
            self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
                                    self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5), outline="#f00",
                                    fill="#f00")


game_instance = Board(8,4)
game_instance.mainloop()
