import random, math

class NQueenGA:

    def __init__(self, n):
        self.n = n

    def initial_population(self, size):
        return [[random.randint(0, self.n - 1) for _ in range(self.n)] for _ in range(size)]

    def fitness(self, state):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return -conflicts

    def weighted_random_choices(self, population, weights, k=2):
        total = sum(weights)
        probs = [w / total for w in weights]
        return random.choices(population, weights=probs, k=k)

    def reproduce(self, parent1, parent2):
        # Single-point crossover
        n = len(parent1)
        c = random.randint(1, n - 1)
        return parent1[:c] + parent2[c:]

    def mutate(self, child):
        # Mutate by changing one random column to a different row
        col = random.randint(0, self.n - 1)
        new_row = random.randint(0, self.n - 1)
        child[col] = new_row
        return child
