# evoChess

Evolutionary algorithm chess bot with GUI 

## Features
- [x] GUI to visualise games
- [x] [Random](AI/randomAI.py) / [Greedy](AI/greedyAI.py) / [Defensive](AI/defensiveAI.py) / [Stockfish](AI/stockfishAI.py) algorithms
- [x] [Piece Square Table](AI/singleTableAI.py) with alpha-beta pruned minimax
- [x] [Evolutionary Piece Square Table](AI/evoTableAI.py) (See [evolution.py](evolution.py) for evolutionary algorithm)
- [ ] Evolutionary algorithm with NN to evaluate thirds of the board [(Based on this paper)](https://ieeexplore.ieee.org/document/1360168)

# Install Requirements

To install the required python libraries run `pip install -r requirements.txt`

# Running the Program

To run the GUI use `python3 main.py`

To evaluate one bot against another, change the players in the main method of [head2head.py](head2head.py) and then run `python3 head2head.py`
- Or import the Head2Head class in your program as in the main method of [head2head.py](head2head.py)

To play one bot against another, import the ChessMatch class in your program
- Example of use in the main method of [chessMatch.py](chessMatch.py)

# Implement a new bot

1. Create a new file in AI/
2. Create a class in that file that inherits PlayerAI (imported from `AI.playerAI`)
3. Implement the `make_move` method. This should return the move you want to make given a position on the board
