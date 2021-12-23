import time
import pygame.display


types = {' ': 'FLOOR',
         'X': 'WALL',
         'E': 'EXIT'}

cells = {'FLOOR': 2,
         'WALL': 1,
         'EXIT': 0}


class MapCell:
    def __init__(self, _type):
        self.type = _type
        if _type != 'FLOOR':
            self.passwords = []
        else:
            self.passwords = None


class Robot:
    def __init__(self, _x=0, _y=0, _map=None, window=None):
        self.x = _x
        self.y = _y
        self.window = window
        self.map = _map
        self.passwords = []
        self.walls = ['WALL', 'EXIT']
        self.found_exit = False
        self.wall = pygame.image.load('pictures/wall.png')
        self.wall2 = pygame.image.load('pictures/wall2.png')
        self.r2d2 = pygame.image.load('pictures/r2d2-2.png')
        self.opened = pygame.image.load('pictures/opened.png')
        self.closed = pygame.image.load('pictures/closed.png')
        self.congratulations = pygame.image.load('pictures/congratulations.png')

    def show(self):
        width = height = 25
        size = 25
        time.sleep(0.05)
        pygame.display.update()
        self.window.fill((255, 255, 255))
        y = 0
        for row in range(len(self.map)):
            x = 0
            for cell in range(len(self.map[row])):
                # print(f'[{row},{cell}]')
                if self.map[row][cell].type == 'FLOOR':
                    if (cell == self.y) and (row == self.x):
                        # robot
                        self.window.blit(self.r2d2, (x * size, y * size))
                        x += 1
                    else:
                        # road
                        pygame.draw.rect(self.window, (100, 100, 100), (x * size, y * size, width, height))
                        x += 1
                elif self.map[row][cell].type == 'EXIT':
                    self.window.blit(self.closed, (x * size, y * size))
                    x += 1
                else:
                    # wall
                    if len(self.map[row][cell].passwords) > 0:
                        self.window.blit(self.wall2, (x * size, y * size))
                    else:
                        self.window.blit(self.wall, (x * size, y * size))
                    x += 1
            y += 1
        pygame.display.update()

    def move_up(self, steps):
        while steps and (self.x - 1 >= 0) and (self.map[self.x - 1][self.y].type == "FLOOR"):
            self.x -= 1
            self.show()
            steps -= 1
        return steps

    def move_down(self, steps):
        while steps and (self.x + 1 < len(self.map)) and (self.map[self.x + 1][self.y].type == "FLOOR"):
            self.x += 1
            self.show()
            steps -= 1
        return steps

    def move_right(self, steps):
        while steps and (self.y + 1 < len(self.map[self.x])) and (self.map[self.x][self.y + 1].type == "FLOOR"):
            self.y += 1
            self.show()
            steps -= 1
        return steps

    def move_left(self, steps):
        while steps and (self.y - 1 >= 0) and (self.map[self.x][self.y - 1].type == "FLOOR"):
            self.y -= 1
            self.show()
            steps -= 1
        return steps

    def ping_up(self, _type):
        dist = 0
        ch = True
        while ch and self.x - dist > 0:
            ch = False
            if self.map[self.x - dist - 1][self.y].type == "FLOOR":
                ch = True
                dist += 1
        if _type is None:
            return dist
        elif self.x - dist > 0:
            if (_type == cells['WALL']) and (self.map[self.x - dist][self.y].type == "WALL"):
                return dist
            elif (_type == cells['EXIT']) and (self.map[self.x - dist-1][self.y].type == "EXIT"):
                return dist
        else:
            return None

    def ping_down(self, _type):
        dist = 0
        ch = True
        while ch and self.x + dist + 1 < len(self.map):
            ch = False
            if self.map[self.x + dist + 1][self.y].type == "FLOOR":
                ch = True
                dist += 1
        if _type is None:
            return dist
        elif self.x + dist + 1 < len(self.map):
            if (_type == cells['WALL']) and (self.map[self.x + dist + 1][self.y].type == "WALL"):
                return dist
            elif (_type == cells['EXIT']) and (self.map[self.x + dist + 1][self.y].type == "EXIT"):
                return dist
        return None

    def ping_right(self, _type):
        dist = 0
        ch = True
        while ch and self.y + dist + 1 < len(self.map[self.x]):
            ch = False
            if self.map[self.x][self.y + dist + 1].type == "FLOOR":
                ch = True
                dist += 1
        if _type is None:
            return dist
        elif self.y + dist + 1 < len(self.map[self.x]):
            if (_type == cells['WALL']) and (self.map[self.x][self.y + dist+1].type == "WALL"):
                return dist
            elif (_type == cells['EXIT']) and (self.map[self.x][self.y + dist+1].type == "EXIT"):
                return dist
        return None

    def ping_left(self, _type):
        dist = 0
        ch = True
        while ch and self.y - dist > 0:
            ch = False
            if self.map[self.x][self.y - dist - 1].type == "FLOOR":
                ch = True
                dist += 1
        if _type is None:
            return dist
        elif self.y - dist > 0:
            if (_type == cells['WALL']) and (self.map[self.x][self.y - dist].type == "WALL"):
                return dist
            elif (_type == cells['EXIT']) and (self.map[self.x][self.y - dist].type == "EXIT"):
                return dist
        return None

    def vision(self):
        passwords = []
        if self.y > 0:
            if self.map[self.x][self.y - 1].type == 'WALL':
                for psw in self.map[self.x][self.y - 1].passwords:
                    passwords.append(psw)
        if self.y + 1 < len(self.map[self.x]):
            if self.map[self.x][self.y + 1].type == 'WALL':
                for psw in self.map[self.x][self.y + 1].passwords:
                    passwords.append(psw)
        if self.x > 0:
            if self.map[self.x - 1][self.y].type == 'WALL':
                for psw in self.map[self.x - 1][self.y].passwords:
                    passwords.append(psw)
        if self.x + 1 < len(self.map):
            if self.map[self.x + 1][self.y].type == 'WALL':
                for psw in self.map[self.x + 1][self.y].passwords:
                    passwords.append(psw)
        return passwords

    def voice(self, password):
        if self.map[self.x][self.y - 1].type == 'EXIT':
            if password in self.map[self.x][self.y - 1].passwords:
                self.found_exit = True
                self.window.blit(self.opened, ((self.y - 1) * 25),  self.x * 25)
        if self.map[self.x][self.y + 1].type == 'EXIT':
            if password in self.map[self.x][self.y + 1].passwords:
                self.found_exit = True
                self.window.blit(self.opened, ((self.y + 1) * 25), self.x * 25)
        if self.map[self.x - 1][self.y].type == 'EXIT':
            if password in self.map[self.x - 1][self.y].passwords:
                self.found_exit = True
                self.window.blit(self.opened, (self.y * 25, (self.x - 1) * 25))
        if self.map[self.x + 1][self.y].type == 'EXIT':
            if password in self.map[self.x + 1][self.y].passwords:
                self.found_exit = True
                self.window.blit(self.opened, (self.y * 25, (self.x + 1) * 25))
        if self.found_exit:
            print(f'Докладываю!!! К выходу [{self.x},{self.y}] подобрал пароль: {password}')
            pygame.display.update()
            time.sleep(0.900)
            self.window.blit(self.congratulations, (0, 0))
            pygame.display.update()
        else:
            print("Кажется, я тут застрял")
