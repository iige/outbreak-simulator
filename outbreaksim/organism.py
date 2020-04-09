import random

directions = ['N', 'E', 'S', 'W', 'NE', 'SE', 'NW', 'SW']


class Organism:
    def __init__(self, Pm, Pd):
        self.r = None
        self.c = None
        self.Pm = Pm
        self.Pd = Pd
        self.healthy = True
        self.just_infected = False
        self.immune = False
        self.mobile = True
        self.remaining_time = 0
        self.direction = None
        self.choose_direction()

    def make_sick(self, K):
        self.healthy = False
        self.remaining_time = round(random.expovariate(1/K))

    def recover(self):
        self.healthy = True
        self.immune = True

    def infect(self, target):
        target.just_infected = True

    def should_die(self):
        return random.random() < self.Pd

    def set_position(self, row, col):
        self.r = row
        self.c = col

    def get_position(self):
        return self.r, self.c

    def set_mobility(self, isMobile):
        self.mobile = isMobile

    def choose_direction(self):
        direction = random.choice(directions)
        while direction is self.direction:
            direction = random.choice(directions)
        self.direction = direction

    def next_position(self):
        next_row = self.r
        next_col = self.c

        if 'N' in self.direction:
            next_row -= 1
        if 'S' in self.direction:
            next_row += 1
        if 'E' in self.direction:
            next_col += 1
        if 'W' in self.direction:
            next_col -= 1

        return next_row, next_col

    def should_move(self):
        return random.random() < self.Pm
