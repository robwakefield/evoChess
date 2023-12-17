#!/usr/bin/env python

from playerAI import PlayerAI
import chess
import random

class GreedyAI(PlayerAI):
    
    def __init__(self):
       self.name = "Greedy"
  
    def make_move(self, board: chess.Board): 
        # For each opponent piece see if we can take it (starting from highest value)
        opp_color = 1 - board.turn
        for type in reversed(chess.PIECE_TYPES):
          for to_square in board.pieces(color=opp_color, piece_type=type):
             if board.is_attacked_by(board.turn, to_square):
                for from_square in board.attackers(board.turn, to_square):
                   move = chess.Move(from_square, to_square)
                   if move in board.legal_moves:
                      return move
        
        # Choose random legal move as backup
        return self.get_random_move(board)
    
    def get_random_move(self, board):
        # Get valid moves and choose random one
        legal_moves = list(board.legal_moves)
        
        move = None
        if legal_moves:
          move = legal_moves[random.randint(0, len(legal_moves)-1)]
        
        return move
