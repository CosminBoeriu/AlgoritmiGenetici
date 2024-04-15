import math
from chromosome import *
import random


class Evolution:
    def __init__(self, function_parameters, num_of_individuals, domain, precision, probabilities, maximum_step,
                 current_step, previous_generation=None):
        self._function_parameters = function_parameters
        self._number_of_individuals = num_of_individuals
        self._domain = domain
        self._precision = precision
        self._recombination_probability = probabilities[0]
        self._mutation_probability = probabilities[1]
        self._final_step = maximum_step
        self._current_step = current_step
        self._number_of_bits = math.ceil(math.log2((domain[1] - domain[0]) * (10 ** precision)))
        if previous_generation is None:
            self._generation = self.generate_first_set_of_individuals()
        else:
            self._generation = previous_generation
        self._probability_distribution = None

    def __str__(self):
        pairs = [(self.evaluate_chromosome(x), x.get_value()) for x in self._generation]
        pairs.sort(reverse=True)
        result = f"Generation number {self._current_step}, it has {len(self._generation)} individuals \n"
        for x in pairs:
            result = result + f"{x[1]} -> {x[0]}\n"
        return result

    def evaluate_chromosome(self, chromosome):
        val = chromosome.get_value()
        return self._function_parameters[0] * val ** 2 + self._function_parameters[1] * val + \
            self._function_parameters[2]

    def generate_first_set_of_individuals(self):
        return [Chromosome((random.uniform(self._domain[0], self._domain[1])))
                for _ in range(self._number_of_individuals)]

    def select_elite_member(self):
        return self._generation[[self.evaluate_chromosome(x) for x in self._generation].index(
            max([self.evaluate_chromosome(x) for x in self._generation]))]

    def assign_probabilities(self):
        minimum_value = min([self.evaluate_chromosome(x) for x in self._generation])
        summation_of_all_values = sum([self.evaluate_chromosome(x) for x in self._generation]) - self._number_of_individuals * minimum_value
        if summation_of_all_values == 0:
            summation_of_all_values = 0.00001
        self._probability_distribution = []
        for ch in self._generation:
            self._probability_distribution.append((self.evaluate_chromosome(ch) - minimum_value) / summation_of_all_values)
        for index, value in enumerate(self._probability_distribution):
            if index == 0:
                self._probability_distribution[index] = (0, value)
            else:
                self._probability_distribution[index] = (self._probability_distribution[index - 1][1],
                                                         self._probability_distribution[index - 1][1] + value)
        self._probability_distribution[-1] = (self._probability_distribution[-1][0], 1)

    def cross_over(self, individuals):
        result = []
        for i in range(len(individuals)):
            breaking_point = random.randint(0, self._number_of_bits - 1)
            left_part = individuals[i].get_segment_of_bits(breaking_point, self._number_of_bits - breaking_point)
            right_part = individuals[(i + 1) % len(individuals)].get_segment_of_bits(0, breaking_point)
            result.append(Chromosome(Chromosome.decode_bit_representation_to_float(left_part + right_part)))
        return result

    def mutation(self, individuals):
        bits = [random.randint(0, self._number_of_bits - 1) for _ in range(len(individuals))]
        return [individuals[i].flip_bit(bits[i]) for i in range(len(individuals))]

    def generate_new_individuals(self):
        intermediate_population = []
        random_numbers = [random.random() for _ in range(self._number_of_individuals - 1)]

        # Selectarea indivizilor din vechea generatie care au sansa de a participa la mutatie si cross-over
        for value in random_numbers:
            left = 0
            right = len(self._probability_distribution) - 1
            while left <= right:
                middle = (left + right) // 2
                try:
                    if self._probability_distribution[middle][0] <= value <= self._probability_distribution[middle][1]:
                        intermediate_population.append(self._generation[middle])
                        debug_flag = True
                        break
                    elif self._probability_distribution[middle][0] > value:
                        right = middle - 1
                    else:
                        left = middle + 1
                except IndexError:
                    pass

        # Procesul de mutatie si cross-over
        cross_over_population = []
        mutation_population = []
        delete_list = []
        for individual in intermediate_population:
            if random.random() < self._recombination_probability:
                cross_over_population.append(individual)
            if random.random() < self._mutation_probability:
                mutation_population.append(individual)
        for x in delete_list:
            intermediate_population.remove(x)
        intermediate_population.append(self.select_elite_member())
        mutated = self.mutation(mutation_population) + self.cross_over(cross_over_population)
        mutated = [x for x in mutated if self._domain[0] <= x.get_value() <= self._domain[1]]
        intermediate_population.sort(reverse=True, key=lambda obj: self.evaluate_chromosome(obj))
        return intermediate_population[0:self._number_of_individuals - len(mutated)] + mutated

    def evolve(self):
        if self._current_step == self._final_step:
            print("Evolution has reached its limit")
            return None
        self.assign_probabilities()
        new_gen = self.generate_new_individuals()
        print(len(new_gen))
        return Evolution(self._function_parameters, self._number_of_individuals, self._domain, self._precision,
                         (self._recombination_probability, self._mutation_probability), self._final_step,
                         self._current_step + 1, new_gen)
