#!/usr/bin/env python

import sys
from AI.playerAI import PlayerAI
import chess
import random
from math import exp, sqrt

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

"""
Updates piece square tables and piece material values using an evolutionary algorithm
"""
class EvoTableAI(PlayerAI):
    
    def __init__(self, depth=2, material_val={}, table={},
                 material_strat_param={}, table_strat_param={}):
        self.name = "Evo Table (d={})".format(depth)
        self.depth = depth
        self.in_endgame = False
        
        self.num_params = 64 * len(chess.PIECE_TYPES) + len(chess.PIECE_TYPES) - 1
        self.tau = 1 / sqrt(2 * self.num_params)
        
        self.MATERIAL_VAL = material_val
        self.MATERIAL_VAL[chess.KING] = 20000
        self.material_strat_param = material_strat_param
        self.TABLE = table
        self.table_strat_param = table_strat_param

        if table == {}:
            self.init_random()
       
    """
    Init random piece values and PSTs
    We also initialise strategy parameters for use during mutation
    """
    def init_random(self):
        for type in chess.PIECE_TYPES:
            if type != chess.KING:
                self.MATERIAL_VAL[type] = random.randint(0, 1000)
                self.material_strat_param[type] = random.uniform(0, 0.05)
            self.TABLE[type] = [random.randint(-50, 50) for _ in range(64)]
            self.table_strat_param[type] = [random.uniform(0, 0.05) for _ in range(64)]
    
    def make_move(self, board: chess.Board):
        # Update search depth when in endgame
        self.in_endgame = self.is_endgame(board)
        if self.in_endgame and self.depth == 2:
            self.depth = 4

        legal_moves = list(board.legal_moves)
        assert len(legal_moves) > 0
        
        best_move = legal_moves[0]
        best_score = INT_MIN
        for move in legal_moves:
            board.push(move)
            score = self.alphabeta(board, self.depth, color=1-board.turn)
            board.pop()
            if score > best_score:
                best_move = move
                best_score = score
        #print("best move", best_move, "score", best_score)
        return best_move
  
    def alphabeta(self, board: chess.Board, depth, color, alpha=INT_MIN, beta=INT_MAX, mini=True):
        if board.is_game_over():
            if board.outcome().winner == None:
                return 0
            elif board.outcome().winner == board.turn:
                return INT_MIN
            else:
                return INT_MAX
    
        if depth == 0:
            return self.evaluate_pos(board, color)

        legal_moves = list(board.legal_moves)
        assert len(legal_moves) > 0
        
        value = INT_MAX if mini else INT_MIN
        for move in legal_moves:
            board.push(move)
            child_score = self.alphabeta(board, depth=depth - 1, color=color, alpha=alpha, beta=beta, mini=not mini)
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
        max_material = self.MATERIAL_VAL[chess.BISHOP] + self.MATERIAL_VAL[chess.QUEEN] + self.MATERIAL_VAL[chess.KING]
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
            material += len(pieces) * self.MATERIAL_VAL[type]
        return material
            
    """
    Evaluate our position using material value and PSTs
    """
    def evaluate_pos(self, board: chess.Board, color: chess.Color):
        material = self.material_value(color, board)
        positional = 0
        for type in reversed(chess.PIECE_TYPES):
            squares = board.pieces(type, color)

            table = self.TABLE[type] if color == chess.WHITE else list(reversed(self.TABLE[type]))
            
            for square in squares:
                positional += table[square]

        return material + positional

    def inc_strat_param(self, s, tau):
        return s * tau * exp(random.normalvariate(0, 1))

    def gen_offspring(self):
        child_material_val = {}
        child_material_strat_param = {}
        child_table = {}
        child_table_strat_param = {}

        for type in chess.PIECE_TYPES:
            # Piece value
            if type != chess.KING:
                s = self.material_strat_param[type]
                s_new = self.inc_strat_param(s, self.tau)
                child_material_strat_param[type] = s_new

                N = random.normalvariate(mu=0, sigma=s_new)
                child_material_val[type] = max(0, self.MATERIAL_VAL[type] + N)
            # PSTs
            child_table[type] = [0] * 64
            child_table_strat_param[type] = [0] * 64
            for i, square in enumerate(self.TABLE[type]):
                s = self.table_strat_param[type][i]
                s_new = self.inc_strat_param(s, self.tau)
                child_table_strat_param[type][i] = s_new

                N = random.normalvariate(mu=0, sigma=s_new)
                child_table[type][i] = square + N
        
        return EvoTableAI(material_val=child_material_val, table=child_table,
                           material_strat_param=child_material_strat_param, 
                           table_strat_param=child_table_strat_param)
