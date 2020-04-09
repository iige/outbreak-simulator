from .organism import Organism
import random


class Simulation:
    def __init__(self, options):
        self.T = 0
        self.N = options['N']
        self.M = options['M']
        self.X = options['X']
        self.S = options['S']
        self.K = options['K']
        self.Pm = options['Pm']
        self.Pd = options['Pd']
        self.population = None
        self.total_infection_rate = 0.0
        self.max_infection_rate = 0.0
        self.max_infection_time = 0
        self.total_infected = 0
        self.total_deaths = 0
        self.matrix = [[None for j in range(self.N)] for i in range(self.N)]

    # Set up the grid and initial population according to options
    def initialize_population(self):
        sickCount = round(self.X * self.M)
        healthyCount = self.M - sickCount
        stationaryCount = round(self.S * self.M)

        population = []

        for i in range(sickCount):
            o = Organism(self.Pm, self.Pd)
            o.make_sick(self.K)
            population.append(o)
            self.total_infected += 1

        for i in range(healthyCount):
            population.append(Organism(self.Pm, self.Pd))

        random.shuffle(population)

        for i in range(stationaryCount):
            population[i].set_mobility(False)

        for organism in population:
            r = random.randrange(0, self.N)
            c = random.randrange(0, self.N)
            while self.matrix[r][c] is not None:
                r = random.randrange(0, self.N)
                c = random.randrange(0, self.N)

            organism.set_position(r, c)
            self.matrix[r][c] = organism

        self.population = population

    # Check if organism has hit a wall or another organism
    # Returns:
    # (Bool, Organism) and Organism might be None
    def collision_check(self, row, col):
        if row < 0 or row > self.N - 1:
            return True, None

        if col < 0 or col > self.N - 1:
            return True, None

        target = self.matrix[row][col]

        if target is not None:
            return True, target

        return False, None

    # Transmit the virus between two organisms if applicable
    def transmission(self, organism1: Organism, organism2: Organism):
        if organism1.healthy is False and organism2.healthy is True:
            organism1.infect(organism2)
            self.total_infected += 1
            return True

        elif organism2.healthy is False and organism1.healthy is True:
            organism2.infect(organism1)
            self.total_infected += 1
            return True

        return False

    def kill(self, organism: Organism):
        row, col = organism.get_position()
        self.matrix[row][col] = None
        self.population.remove(organism)
        self.total_deaths += 1

    def all_healthy(self):
        for organism in self.population:
            if not organism.healthy:
                return False
        return True

    # Check the current board to see if any state changes need to occur
    def update(self):
        self.T += 1
        for organism in self.population:
            if organism.just_infected and not organism.immune:
                organism.make_sick(self.K)
                organism.just_infected = False
            elif not organism.healthy:
                organism.remaining_time -= 1
                if organism.remaining_time <= 0:
                    if organism.should_die():
                        self.kill(organism)
                        self.total_deaths += 1
                    else:
                        organism.recover()

    # Advance through a time period within the board
    # Returns:
    # Bool - whether or not new infections have occured
    def step(self):
        self.update()
        self.update_stats()
        new_infections = False
        for organism in self.population:
            if organism.mobile and organism.should_move():
                next_row, next_col = organism.next_position()
                check = self.collision_check(next_row, next_col)

                collided = check[0]
                target = check[1]

                if not collided:
                    current_row, current_col = organism.get_position()
                    self.matrix[current_row][current_col] = None
                    organism.set_position(next_row, next_col)
                    self.matrix[next_row][next_col] = organism
                else:
                    if target is not None:
                        new_infection = self.transmission(organism, target)
                        if new_infection and new_infections is False:
                            new_infections = True
                    organism.choose_direction()
        return new_infections

    def update_stats(self):
        num_infected = 0
        for organism in self.population:
            if not organism.healthy:
                num_infected += 1

        infection_rate = num_infected / len(self.population)

        if infection_rate > self.max_infection_rate:
            self.max_infection_rate = infection_rate
            self.max_infection_time = self.T

    def print(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                organism = self.matrix[i][j]
                if organism is None:
                    print(' -- ', end='')
                else:
                    if organism.healthy:
                        if organism.mobile:
                            print(' HM ', end='')
                        else:
                            print(' HS ', end='')
                    else:
                        if organism.mobile:
                            print(' IM ', end='')
                        else:
                            print(' IS ', end='')
            print('')
