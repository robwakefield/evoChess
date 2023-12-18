#!/usr/bin/env python

from AI.playerAI import PlayerAI
import chess
import random

"""
Tries not to lose pieces by moving attacked pieces.
Will always choose a move that leads to a draw.
"""
class DefensiveAI(PlayerAI):
    
    def __init__(self):
       self.name = "Defensive"
  
    def make_move(self, board: chess.Board): 
        # Try to draw
        legal_moves = list(board.legal_moves)
        if legal_moves != None:
            for move in legal_moves:
                board.push(move)
                if board.is_game_over() and board.outcome().winner == None:
                    board.pop()
                    return move
                board.pop()

        # Defend pieces by moving them (higest value first)
        opp_color = 1 - board.turn
        for type in reversed(chess.PIECE_TYPES):
          for from_square in board.pieces(color=board.turn, piece_type=type):
             if board.is_attacked_by(opp_color, from_square):
                for to_square in board.attacks(from_square):
                   move = chess.Move(from_square, to_square)
                   if move in board.legal_moves:
                        board.push(move)
                        # If the move does not save our piece, we do not move there
                        if not board.is_attacked_by(opp_color, from_square):
                            board.pop()
                            return move
                        else:
                            board.pop()
        
        # Choose random legal move as backup
        return self.get_random_move(board)
    
    def get_random_move(self, board: chess.Board):
        # Get valid moves and choose random one
        legal_moves = list(board.legal_moves)
        
        if legal_moves == None:
          return None
        
        return legal_moves[random.randint(0, len(legal_moves)-1)]
        