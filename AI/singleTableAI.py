#!/usr/bin/env python

import sys
from AI.playerAI import PlayerAI
import chess
import AI.PST as PST

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

"""
Uses piece square tables with alpha-beta pruned minimax to evaluate each legal move
"""
class SingleTableAI(PlayerAI):
    
    def __init__(self, depth=2):
       self.name = "Single Table (d={})".format(depth)
       self.depth = depth
       self.in_endgame = False

    def make_move(self, board: chess.Board):
        # Update search depth when in endgame
        if self.in_endgame and self.depth == 2:
            self.depth = 4

        legal_moves = list(board.legal_moves)
        assert len(legal_moves) > 0
        
        best_move = legal_moves[0]
        best_score = INT_MIN
        for move in legal_moves:
            board.push(move)
            score = self.alphabeta(board, self.depth)
            board.pop()
            if score > best_score:
                best_move = move
                best_score = score
        #print("best move", best_move, "score", best_score)
        return best_move
  
    def alphabeta(self, board: chess.Board, depth, alpha=INT_MIN, beta=INT_MAX, mini=True):
        if board.is_game_over():
            if board.outcome().winner == None:
                return 0
            elif board.outcome().winner == board.turn:
                return INT_MIN
            else:
                return INT_MAX
    
        if depth == 0:
            return self.evaluate_pos(board, 1-board.turn)

        legal_moves = list(board.legal_moves)
        assert len(legal_moves) > 0
        
        value = INT_MAX if mini else INT_MIN
        for move in legal_moves:
            board.push(move)
            child_score = self.alphabeta(board, depth=depth - 1, alpha=alpha, beta=beta, mini=not mini)
            board.pop()
            if mini:
                value = min(value, child_score)
                if value < alpha:
                    # alpha cutoff
                    break
                beta = min(beta, value)
            else:
                value = max(value, child_score)
                if value > beta:
                    # beta cutoff
                    break
                alpha = max(alpha, value)

        return value
    
    """
    Check if endgame is entered
    """
    def is_endgame(self, board: chess.Board):
        # Both sides have no queens
        if len(board.pieces(chess.QUEEN, chess.WHITE)) == 0 and len(board.pieces(chess.QUEEN, chess.BLACK)) == 0:
            return True
        # Or every side which has a queen has additionally no other pieces or one minorpiece maximum.
        max_material = PST.MATERIAL_VAL[chess.BISHOP] + PST.MATERIAL_VAL[chess.QUEEN] + PST.MATERIAL_VAL[chess.KING]
        for color in chess.COLORS:
            if len(board.pieces(chess.QUEEN, color)) == 1 and self.material_value(color, board) > max_material:
                return False
        return True

    """
    Return the centipawn piece value of a board for a given color
    """
    def material_value(self, color: chess.Color, board: chess.Board):
        material = 0
        for type in reversed(chess.PIECE_TYPES):
            pieces = board.pieces(type, color)
            material += len(pieces) * PST.MATERIAL_VAL[type]
        return material
            
    """
    Evaluate our position using material value and PSTs
    """
    def evaluate_pos(self, board: chess.Board, color: chess.Color):
        self.in_endgame = self.is_endgame(board)
        material = self.material_value(color, board)
        positional = 0
        for type in reversed(chess.PIECE_TYPES):
            squares = board.pieces(type, color)

            table = PST.TABLE[type] if color == chess.WHITE else list(reversed(PST.TABLE[type]))
            # Choose KING table based on stage of game
            if type == chess.KING and self.in_endgame:
                table = PST.KING_END if color == chess.WHITE else list(reversed(PST.KING_END))
            
            for square in squares:
                positional += table[square]

        return material + positional

               
               


        