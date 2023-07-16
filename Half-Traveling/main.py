import math
import random
import time

def read_cities(filename):
    cities = []
    with open(filename, 'r') as f:
        for line in f:
            city = list(map(int, line.split()))  # Convert the line to a list of integers
            cities.append(city)  # Append the city to the list of cities
    return cities

def dist(city1, city2):
    dx = city1[1] - city2[1]
    dy = city1[2] - city2[2]
    return math.sqrt(dx*dx + dy*dy)  # Calculate the Euclidean distance

def tour_length(tour, cities):
    length = sum(dist(cities[tour[i]], cities[tour[i - 1]]) for i in range(len(tour)))
    return length  # Calculate the total length of the tour

def generate_neighbour(tour):
    N = len(tour)
    i, j = random.sample(range(N), 2)  # Randomly select two cities to swap
    neighbour_tour = tour[:]  # Create a copy of the current tour
    neighbour_tour[i], neighbour_tour[j] = neighbour_tour[j], neighbour_tour[i]  # Swap the cities
    return neighbour_tour  # Return the new tour

def write_tour_to_txt(tour, cities, filename):
    with open(filename, 'w') as f:
        f.write(str(int(tour_length(tour, cities))) + '\n')  # Write the tour length as the first line
        for city in tour:
            f.write(str(city) + '\n')  # Write each city ID on a new line

def checksolution(cities, value, cityorder):
    n = len(cities)
    cityorder_sorted = list(cityorder)
    cityorder_sorted.sort()  # Sort the city order to check for duplicates
    n_half = len(cityorder_sorted)

    # Check if the tour contains exactly n/2 cities
    if n_half != len(cityorder):
        print('ERROR: Not a half tour')
        exit()
    else:
        for i in range(len(cityorder)-1):
            # Check for duplicate cities
            if cityorder_sorted[i] == cityorder_sorted[i+1]:
                print('ERROR: There are duplicate cities')
                exit()
        for i in range(len(cityorder)):
            # Check for invalid city IDs
            if (cityorder[i] < 0) or (cityorder[i] >= n):
                print('ERROR: Invalid city id: ', cityorder[i])
                exit()

    # Calculate the length of the tour given by cityorder
    dist = tour_length(cityorder, cities)

    # Check the value of the solution
    if dist == value:
        print('Your solution is VERIFIED.')
    else:
        print('Your solution is NOT VERIFIED.')
        print('Your solution length given as', value)
        print('but computed as', dist)

def main():
    file_pairs = [('test-input-1.txt', 'test-output-1.txt'),
                  ('test-input-2.txt', 'test-output-2.txt'),
                  ('test-input-3.txt', 'test-output-3.txt'),
                  ('test-input-4.txt', 'test-output-4.txt')]

    for input_file, output_file in file_pairs:
        cities = read_cities(input_file)  # Read the cities from the input file

        N = len(cities)
        half_N = int(math.ceil(N / 2.0))  # Calculate the half size of the cities

        current_tour = list(range(half_N))  # Initialize the current tour

        T = 10000
        alpha = 0.9995
        T_end = 0.01

        start_time = time.time()  # Start measuring the execution time

        while T > T_end:
            T *= alpha  # Update the temperature

            current_length = tour_length(current_tour, cities)  # Calculate the length of the current tour
            new_tour = generate_neighbour(current_tour)  # Generate a new neighboring tour
            new_length = tour_length(new_tour, cities)  # Calculate the length of the new tour

            if new_length < current_length or math.exp((current_length - new_length) / T) > random.random():
                current_tour = new_tour  # Accept the new tour if it is shorter or based on a probability

        print("Execution time for {}: {}".format(input_file, time.time() - start_time))  # Print the execution time

        write_tour_to_txt(current_tour, cities, output_file)  # Write the resulting tour to the output file

        # Verify the solution
        checksolution(cities, tour_length(current_tour, cities), current_tour)

main()
