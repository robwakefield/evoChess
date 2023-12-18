#!/usr/bin/env python

from playerAI import PlayerAI
import random

class RandomAI(PlayerAI):
    
    def __init__(self):
       self.name = "Random"

    def make_move(self, board): 
        # Get valid moves and choose random one
        legal_moves = list(board.legal_moves)
        
        move = None
        if legal_moves:
          move = legal_moves[random.randint(0, len(legal_moves)-1)]
        
        return move