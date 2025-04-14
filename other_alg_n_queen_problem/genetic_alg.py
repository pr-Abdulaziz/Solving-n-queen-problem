import random

def solve(geneticNQ):
    return genetic_alg(geneticNQ, 100, 1000, 0.1)

def genetic_alg(alg, pop_size, generations, rate):
    population = alg.initial_population(pop_size)

    for i in range(generations):
        fitness_scores = [alg.fitness(ind) for ind in population]
        
        # Check for solution
        best = max(zip(population, fitness_scores), key=lambda x: x[1])
        if best[1] == 0:
            return best[0]
        
        # Create new population
        new_population = []
        for _ in range(pop_size):
            parent1, parent2 = alg.weighted_random_choices(population, [f + 1e-6 for f in fitness_scores])  # avoid zero weights
            child = alg.reproduce(parent1, parent2)
            if random.random() < rate:
                child = alg.mutate(child)
            new_population.append(child)

        population = new_population
        
    # Return best found
    fitness_scores = [alg.fitness(ind) for ind in population]
    best = max(zip(population, fitness_scores), key=lambda x: x[1])
    return best[0]
