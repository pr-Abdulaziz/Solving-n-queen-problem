import random
class NQueen:

    def __init__(self, n):
        self.n = n
    
    def initial_state(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def value(self, state):
        return self.attacking_pairs(state)

    def attacking_pairs(self, state):
        count = 0
        for i in range(self.n):
            for j in range(1, self.n):
                if state[i] == state[j] or abs(i-j) == abs(state[i]-state[j]):
                    count += 1

        return count


    def neighbors(self, state):
        all_neighbors = list()

        for column in range(self.n):
            for row in range(self.n):
                if state[column] != row:
                    new_state = list(state)
                    new_state[column] = row
                    all_neighbors.append(new_state)
        return all_neighbors


    
