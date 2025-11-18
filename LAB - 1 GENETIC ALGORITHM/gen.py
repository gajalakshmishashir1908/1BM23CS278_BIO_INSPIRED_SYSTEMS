import random

# Set random seed for reproducibility
random.seed(42)

# Generate a random population of chromosomes
def generate_random_population(pop_size, num_jobs):
    population = []
    for _ in range(pop_size):
        chromosome = list(range(num_jobs))
        random.shuffle(chromosome)  # Randomly shuffle jobs
        population.append(chromosome)
    return population

# Calculate the makespan (fitness function)
def calculate_makespan(chromosome, job_times):
    completion_time = 0
    for job_index in chromosome:
        completion_time += job_times[job_index]
    return completion_time

# Fitness function: Minimize makespan
def fitness(chromosome, job_times):
    makespan = calculate_makespan(chromosome, job_times)
    return 1 / (makespan + 1)  # Inverse of makespan

# Tournament Selection: Select two individuals based on fitness
def tournament_selection(population, job_times, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: -fitness(x, job_times))  # Sort by fitness (descending)
    return tournament[0], tournament[1]  # Return the top 2 individuals

# Order Crossover (OX) for job scheduling
def order_crossover(parent1, parent2):
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size

    # Select two random crossover points
    cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

    # Copy the slice from parent1 to child1 and parent2 to child2
    child1[cx_point1:cx_point2] = parent1[cx_point1:cx_point2]
    child2[cx_point1:cx_point2] = parent2[cx_point1:cx_point2]

    # Fill the remaining positions
    fill_parent(child1, parent2, cx_point1, cx_point2)
    fill_parent(child2, parent1, cx_point1, cx_point2)

    return child1, child2

# Helper function to fill in missing genes after crossover
def fill_parent(child, parent, start, end):
    size = len(child)
    current_pos = end
    for i in range(size):
        if parent[i] not in child:
            if current_pos >= size:
                current_pos = 0
            child[current_pos] = parent[i]
            current_pos += 1

# Mutation function (Swap two jobs)
def mutate(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

# Main Genetic Algorithm
def genetic_algorithm(job_times, pop_size=100, generations=1000, Pc=0.8, Pm=0.1):
    num_jobs = len(job_times)
    
    # Initialize population
    population = generate_random_population(pop_size, num_jobs)

    best_solution = None
    best_fitness = -float('inf')

    for gen in range(generations):
        new_population = []
        
        # Create new population through crossover and mutation
        while len(new_population) < pop_size:
            parent1, parent2 = tournament_selection(population, job_times)
            if random.random() < Pc:
                child1, child2 = order_crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            if random.random() < Pm:
                mutate(child1)
            if random.random() < Pm:
                mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        # Replace old population with new population
        population = new_population

        # Evaluate the fitness of the population
        for individual in population:
            individual_fitness = fitness(individual, job_times)
            if individual_fitness > best_fitness:
                best_fitness = individual_fitness
                best_solution = individual

        # Print progress
        print(f"Generation {gen+1}: Best Fitness = {best_fitness}")

    return best_solution, 1 / best_fitness

# Example usage
if __name__ == "__main__":
    job_times = [3, 2, 4, 5, 1]  # Processing times for each job
    best_solution, best_makespan = genetic_algorithm(job_times)
    print(f"Best Job Order: {best_solution}")
    print(f"Best Makespan: {best_makespan}")
