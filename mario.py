import numpy as np
from copy import deepcopy
import random
from itertools import combinations
from tkinter import *
import numpy as np

size_of_board = 400
Green_color = '#7BC043'


# class Board():
#     def __init__(self, n, m,RM,BM,O):
#         self.n = n
#         self.m = m
#         self.window = Tk()
#         self.window.title('Mushroom Eater!')
#         self.w = int(size_of_board / max(self.m, self.n))
#         self.canvas = Canvas(self.window, width=self.w * self.m + 100, height=self.w * self.n)
#         self.canvas.pack()
#         self.window.bind('<Button-1>', self.click)
#         self.initialize_board(RM,BM,O)
#
#     def mainloop(self):
#         self.window.mainloop()
#
#     def initialize_board(self, RedMushrooms, BlueMushrooms, obstacles):
#         for i in range(self.m):
#             self.canvas.create_line((i + 1) * self.w, 0, self.w * (i + 1), self.w * self.n)
#         for i in range(self.n):
#             self.canvas.create_line(0, (i + 1) * self.w, self.w * self.m, (i + 1) * self.w)
#         for t in obstacles:
#             x=t[0]
#             y=t[1]
#             self.canvas.create_rectangle(self.w * x, self.w * y, self.w * (x + 1), self.w * (y + 1), outline="#000",
#                                          fill="#000")
#         for t in RedMushrooms.keys():
#             x = t[0]
#             y = t[1]
#             RedMushrooms[t] = self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
#                                                       self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5),
#                                                       outline="#f00",fill="#f00")
#             print('mushrooom',t,RedMushrooms[t])
#         for t in BlueMushrooms.keys():
#             x = t[0]
#             y = t[1]
#             BlueMushrooms[t] = self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
#                                                        self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5),
#                                                        outline="#00f",
#                                                        fill="#00f")
#
#     def put_mario(self, position):
#         x = position[0]
#         y = position[1]
#         self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
#                                 self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5), outline="#0f0",
#                                 fill="#0f0")
#
#     def removeRed(self, sp, RedMushrooms):
#         print(RedMushrooms[sp],'about to be deleted')
#         self.canvas.delete(RedMushrooms[sp])
#         self.canvas.update()
#
#     def removeBlue(self, sp, BlueMushrooms):
#         print(BlueMushrooms[sp],'about to be deleted')
#         self.canvas.delete(BlueMushrooms[sp])
#         self.canvas.update()
#
#     def move_mario(self,sp):
#         self.canvas.delete(self.last_mario)
#         self.last_mario=self.canvas.create_polygon(sp[0]*self.w,(sp[1]+0.5)*self.w,
#                                    (sp[0]+0.5)*self.w,sp[1]*self.w,
#                                    (sp[0]+1)*self.w,(sp[1]+0.5)*self.w,
#                                    (sp[0]+0.5)*self.w,(sp[1]+1)*self.w,fill="#acf")
#         self.canvas.update()
#
#     def click(self,event):

# --------------------------------------------------

class Agent:
    def __init__(self, n, m, s, k, red_mushrooms, blue_mushrooms, obstacles):
        self.m = m
        self.n = n
        self.acts = {0: [0, 1], 1: [1, 0], 2: [0, -1], 3: [-1, 0]}  # right-up-left-down
        self.action = None
        self.H = np.full((n, m), None)
        self.h = np.full((n, m), None)
        self.s = None
        self.sp = s
        self.k = k
        self.RedMushrooms = red_mushrooms
        self.BlueMushrooms = blue_mushrooms
        self.obstacles = obstacles
        self.result = {}
        self.RedEaten = False
        self.BlueEaten = False
        self.remaining = 2 * k
        self.method = 3
        self.most_distance = 0
        # gui init
        self.window = Tk()
        self.window.title('Mushroom Eater!')
        self.w = int(size_of_board / max(self.m, self.n))
        self.canvas = Canvas(self.window, width=self.w * self.m + 100, height=self.w * self.n)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.initialize_board(RedMushrooms, BlueMushrooms, obstacles)
        self.last_mario = None

    @staticmethod
    def most_dist(RM, BM):
        mushrooms=[]
        for r in RM:
            mushrooms.append(r)
        for b in BM:
            mushrooms.append(b)
        print("mushrooooooooms",mushrooms)
        combs = combinations(mushrooms, 2)
        maximum=0
        for i in combs:
            manhattan = abs(i[0][0] - i[1][0]) + abs(i[1][0] - i[1][1])
            if maximum<manhattan:
                maximum=manhattan
        return maximum

    def cal_heu(self, sp):
        if self.method == 1:
            if sp in self.RedMushrooms or sp in self.BlueMushrooms:
                return self.remaining - 1
            return self.remaining

        elif self.method == 2:
            mini = self.k * self.k
            for mush in self.RedMushrooms:
                manhattan = abs(sp[0] - mush[0]) + abs(sp[1] - mush[1])
                if manhattan < mini:
                    mini = manhattan
            for mush in self.BlueMushrooms:
                manhattan = abs(sp[0] - mush[0]) + abs(sp[1] - mush[1])
                if manhattan < mini:
                    mini = manhattan
            return mini

        elif self.method == 3:
            if sp in self.RedMushrooms.keys():
                print("in red")
                return self.most_dist(list(self.RedMushrooms.keys()).pop(sp), list(self.BlueMushrooms.keys()))
            if sp in self.BlueMushrooms.keys():
                print("in blue")
                return self.most_dist(list(self.BlueMushrooms.keys()).pop(sp),list(self.BlueMushrooms.keys()))
            else:
                print("in white")
                print(list(self.RedMushrooms.keys()))
                print(list(self.BlueMushrooms.keys()))
                return self.most_dist(list(self.RedMushrooms.keys()), list(self.BlueMushrooms.keys()))

    def step(self):
        if self.RedEaten and self.BlueEaten:
            return True
        else:
            self.action = self.LRTA_Agent(deepcopy(self.sp))
            self.s = deepcopy(self.sp)
            sp = self.next(self.s, self.action)
            print("\n\naction:", self.action)
            print("next state:", sp)
            self.move_mario(sp)
            if sp in self.RedMushrooms.keys():
                print('red mushroom at', sp)
                self.RedEaten = True
                self.remaining -= 1
                self.removeRed(sp)
                self.RedMushrooms.pop(sp)
            if sp in self.BlueMushrooms.keys():
                print("blue mushroom at", sp)
                self.BlueEaten = True
                self.remaining -= 1
                self.removeBlue(sp)
                self.BlueMushrooms.pop(sp)
            self.sp = deepcopy(sp)

    def LRTA_Agent(self, sp):
        if not self.H[sp[0]][sp[1]]:
            self.h[sp[0]][sp[1]] = self.H[sp[0]][sp[1]] = self.cal_heu(sp)
        if self.s:
            self.result[(self.s[0], self.s[1], self.action)] = deepcopy(sp)
            m = 1000
            for act in self.acts.keys():
                if (self.s[0], self.s[1], act) in self.result.keys():
                    if self.result[(self.s[0], self.s[1], act)] == (self.s[0], self.s[1]):
                        continue
                cost = self.LRTA_Cost(s, (s[0], s[1], act))
                if m > cost:
                    m = cost
            self.H[self.s[0]][self.s[1]] = m
            print('H', self.s, '=', m)
        mi = 1000
        best_acts = []
        for act in self.acts.keys():
            if (sp[0], sp[1], act) in self.result.keys():
                if self.result[(sp[0], sp[1], act)] == (sp[0], sp[1]):
                    continue
            cost = self.LRTA_Cost(sp, (sp[0], sp[1], act))
            if mi > cost:
                mi = cost
                best_acts = [act]
            elif mi == cost:
                best_acts.append(act)
            print("act:", act, "  cost:", cost)
        return random.choice(best_acts)

    def LRTA_Cost(self, s, res):
        if res not in self.result.keys():
            self.h[s[0]][s[1]] = self.cal_heu(s)
            return self.h[s[0]][s[1]]
        sp = self.next(s, res[2])
        return self.H[sp[0]][sp[1]] + 1

    def next(self, s, a):
        if (s[0], s[1], a) in self.result.keys():
            return self.result[(s[0], s[1], a)]
        statep = [s[0] + self.acts[a][0], s[1] + self.acts[a][1]]
        if statep in self.obstacles or (statep[0] < 0) or statep[0] >= self.m or statep[1] < 0 or statep[1] >= self.n:
            statep = s
        return tuple(statep)

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self, RedMushrooms, BlueMushrooms, obstacles):
        for i in range(self.m):
            self.canvas.create_line((i + 1) * self.w, 0, self.w * (i + 1), self.w * self.n)
        for i in range(self.n):
            self.canvas.create_line(0, (i + 1) * self.w, self.w * self.m, (i + 1) * self.w)
        for t in obstacles:
            x = t[0]
            y = t[1]
            self.canvas.create_rectangle(self.w * x, self.w * y, self.w * (x + 1), self.w * (y + 1), outline="#000",
                                         fill="#000")
        for t in RedMushrooms.keys():
            x = t[0]
            y = t[1]
            RedMushrooms[t] = self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
                                                      self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5),
                                                      outline="#f00", fill="#f00")

        for t in BlueMushrooms.keys():
            x = t[0]
            y = t[1]
            BlueMushrooms[t] = self.canvas.create_oval(self.w * x + (self.w / 5), self.w * y + (self.w / 5),
                                                       self.w * (x + 1) - (self.w / 5), self.w * (y + 1) - (self.w / 5),
                                                       outline="#00f",
                                                       fill="#00f")
        # self.last_mario = self.canvas.create_polygon(s[0] * self.w, (s[1] + 0.5) * self.w,
        #                                              (s[0] + 0.5) * self.w, s[1] * self.w,
        #                                              (s[0] + 1) * self.w, (s[1] + 0.5) * self.w,
        #                                              (s[0] + 0.5) * self.w, (s[1] + 1) * self.w, fill="#acf")

    def removeRed(self, sp):
        self.canvas.delete(self.RedMushrooms[sp])
        self.canvas.update()

    def removeBlue(self, sp):
        self.canvas.delete(self.BlueMushrooms[sp])
        self.canvas.update()

    def move_mario(self, sp):
        self.canvas.delete(self.last_mario)
        self.last_mario = self.canvas.create_polygon(sp[0] * self.w, (sp[1] + 0.5) * self.w,
                                                     (sp[0] + 0.5) * self.w, sp[1] * self.w,
                                                     (sp[0] + 1) * self.w, (sp[1] + 0.5) * self.w,
                                                     (sp[0] + 0.5) * self.w, (sp[1] + 1) * self.w, fill="#acf")
        self.canvas.update()

    def click(self, event):
        self.step()


def get_line(f, n):
    point = list(map(int, f.readline().split()))
    point[0] = point[0] - 1
    point[1] = n - point[1]
    return tuple(point)


with open('Mario.txt') as f:
    n = int(f.readline())
    m = int(f.readline())
    s = get_line(f, n)
    k = int(f.readline())
    BlueMushrooms = {}
    RedMushrooms = {}
    obstacles = []
    for i in range(k):
        BlueMushrooms[get_line(f, n)] = None

    for i in range(k):
        RedMushrooms[get_line(f, n)] = None
    while True:
        line = f.readline()
        if not line:
            break
        p = list(map(int, line.split()))
        if not p:
            break
        p[0] = p[0] - 1
        p[1] = n - p[1]
        obstacles.append(p)

a = Agent(n, m, s, k, RedMushrooms, BlueMushrooms, obstacles)
# a.Algo()
a.mainloop()
