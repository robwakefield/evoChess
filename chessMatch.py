#!/usr/bin/env python

import chess
from AI.playerAI import PlayerAI

from AI.greedyAI import GreedyAI
from AI.randomAI import RandomAI
  
class ChessMatch(): 
  
    def __init__(self, white: PlayerAI, black: PlayerAI):
        self.white_player = white
        self.black_player = black
        self.board = chess.Board()

    def get_player(self):
        return self.white_player if self.board.turn == chess.WHITE else self.black_player

    def play(self, move_limit=None, debug=False):
        if debug:
          print(self.white_player.name, "vs", self.black_player.name)
        plys = 0
        moves = 0
        while not self.board.is_game_over():
            move = self.get_player().make_move(self.board)

            if move not in self.board.legal_moves:
                if debug:
                    print("Illegal Move by", self.get_player().name, move)
                # Gift the other player the win
                return 1 - self.board.turn

            self.board.push(move)
            plys += 1
            moves = plys // 2
            if move_limit != None and moves >= move_limit:
                if debug:
                  print("Move Limit Reached")
                return 0.5
        
        # Game is finished
        if debug:
            print("Outcome", self.board.outcome().result())
        winner = self.board.outcome().winner
        return winner if winner != None else 0.5

if __name__ == "__main__":
    greedy = GreedyAI()
    random = RandomAI()
    match = ChessMatch(greedy, random)
    match.play(debug=True)
