# Install Requirements

To install the required python libraries run `pip install -r requirements.txt`

# Running the Program

To run the GUI use `python3 main.py`

To evaluate an AI against another, change the players in the main method of [head2head.py](head2head.py) and then run `python3 head2head.py`
- Or import the Head2Head class in your program as in the main method of [head2head.py](head2head.py)

To play an AI against another, import the ChessMatch class in your program
- Example of use in the main method of [chessMatch.py](chessMatch.py)

# Implement an AI

1. Create a new file in AI/
2. Create a class in that file that inherits PlayerAI (imported from AI.playerAI)
3. Implement the `make_move` method. This should return the move you want to make
