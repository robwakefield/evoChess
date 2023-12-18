#!/usr/bin/env python

import chess
from AI.playerAI import PlayerAI
from chessMatch import ChessMatch

from AI.greedyAI import GreedyAI
from AI.randomAI import RandomAI
  
class Head2Head(): 
  
    def __init__(self, player1: PlayerAI, player2: PlayerAI):
        self.player1 = player1
        self.player2 = player2

    def evaluate(self, iterations=100):
        # From player1 POV
        wins = 0
        draws = 0
        losses = 0
        
        white = self.player1
        black = self.player2
        for color in chess.COLORS:
          for _ in range(iterations // 2):
              match = ChessMatch(white, black)
              winner = match.play()
              if winner == 0.5:
                  draws += 1
              elif winner == color:
                  wins += 1
              else:
                  losses += 1
          
          # Switch black and white
          white = self.player2
          black = self.player1

        actual_iterations = (iterations // 2) * 2
        win_pc = (wins / actual_iterations) * 100
        loss_pc = (losses / actual_iterations) * 100
        draw_pc = (draws / actual_iterations) * 100

        print(self.player1.name, "win", "{:.1f}%".format(win_pc))
        print(self.player2.name, "win", "{:.1f}%".format(loss_pc))
        print("draws", "{:.1f}%".format(draw_pc))

if __name__ == "__main__":
    greedy = GreedyAI()
    random = RandomAI()
    h2h = Head2Head(greedy, random)
    h2h.evaluate(iterations=1000)