#!/usr/bin/env python

from AI.playerAI import PlayerAI
import chess
from stockfish import Stockfish

SF_PATH = "/opt/homebrew/bin/stockfish"

"""
Runs local version of stockfish installed at self.SF_PATH
"""
class StockfishAI(PlayerAI):
    
    def __init__(self, elo=1350, depth=15, threads=2, time_limit=10, sf_path=SF_PATH):
       self.name = "StockFish({})".format(elo)
       self.time_limit = time_limit
       self.sf = Stockfish(sf_path, depth=depth, parameters={
          "Threads": threads,
       })
       self.sf.set_elo_rating(elo)
  
    def make_move(self, board: chess.Board): 
        # Generate FEN representation of board
        fen = board.fen()
        # Use StockFish to generate the best move
        self.sf.set_fen_position(fen)
        move = chess.Move.from_uci(self.sf.get_best_move_time(self.time_limit))
        return move
        