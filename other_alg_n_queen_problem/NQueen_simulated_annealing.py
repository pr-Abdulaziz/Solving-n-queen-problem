import random, math

def schedule(t, T0=30.0, alpha=0.95):
    return T0 * (alpha ** t)


def simulated_annealing(problem, schedule):

    current_state = problem.initial_state()
    t = 1
    while True:
        T = schedule(t)
        if T == 0:
            return current_state

        next_state = random.choice(problem.neighbors(current_state))
        delta_E = problem.value(current_state)-problem.value(next_state)

        if delta_E > 0:
            current_state = next_state

        else:
            probability = math.exp(delta_E / T)
            if random.random() < probability:
                current_state = next_state

        t += 1
