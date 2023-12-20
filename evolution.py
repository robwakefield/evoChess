#!/usr/bin/env python

import chess
from AI.evoTableAI import EvoTableAI
from chessMatch import ChessMatch
import random
import pickle

class Evolution():
  
    def __init__(self, population_size=10):
        self.pop_size = population_size

    def run(self, generations=5):
        # Initialise population
        population = self.init_population(self.pop_size)
        for gen in range(generations):
            # Randomly vary individuals
            population = self.generate_offspring(population)
            # Evaluate fitness
            fitness = []
            for player in population:
                fitness.append(self.fitness(player, [p for p in population if p != player]))
            print(fitness)
            # Select new generation
            if gen < generations - 1:
                population = self.get_best(zip(fitness, population), size=self.pop_size)
                print("Generation", gen, "complete")
            else:
                # Return best
                return self.get_best(zip(fitness, population), size=1)[0]

    def init_population(self, size):
        return [EvoTableAI() for _ in range(size)]
    
    def generate_offspring(self, parents: list[EvoTableAI]):
        children = [p.gen_offspring() for p in parents]
        return parents + children

    # Play games against population and give score
    def fitness(self, player: EvoTableAI, opponents: list[EvoTableAI]):
        score = 0
        # Play half as White
        for _ in range(1):
            opponent = random.choice(opponents)
            match = ChessMatch(player, opponent)
            outcome = match.play(debug=True)

            if outcome == chess.WHITE:
                score += 1
            elif outcome == chess.BLACK:
                score += 0
            else:
                score += 0.5
    
        # Play half as Black
        for _ in range(1):
            opponent = random.choice(opponents)
            match = ChessMatch(player, opponent)
            outcome = match.play(debug=True)
            
            if outcome == chess.BLACK:
                score += 1
            elif outcome == chess.WHITE:
                score += 0
            else:
                score += 0.5
        
        return score
    
    def get_best(self, population: list[tuple[int, EvoTableAI]], size):
        return [player for _, player in 
                sorted(population, key=lambda tup: tup[0])[:size]]

def save_pickle(model: EvoTableAI):
    with open('best_model', 'wb') as file:
        pickle.dump(model, file)

def load_pickle(file) -> EvoTableAI:
    with open('best_model', 'rb') as file:
        return pickle.load(file)

if __name__ == "__main__":
    print("Loading model")
    model = load_pickle('best_model')
    if isinstance(model, EvoTableAI):
        print("Piece Values", model.MATERIAL_VAL)

    evoluter = Evolution(population_size=2)
    print("Running Evolution")
    best = evoluter.run(generations=1)
    print("Evolution Complete")
    save_pickle(best)

    print("Best Piece Values")
    print(best.MATERIAL_VAL)
    print("Best PSTs")
    print(best.TABLE)
