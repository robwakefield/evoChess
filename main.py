#!/usr/bin/env python

import io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import chess
import chess.svg
import cairosvg

from randomAI import RandomAI
from greedyAI import GreedyAI

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("evoChess")

        # Create chessboard frame
        self.board_size = 400
        self.square_size = self.board_size // 8

        self.chessboard_frame = ttk.Frame(root, width=self.board_size, height=self.board_size)
        self.chessboard_frame.grid(row=0, column=1)

        # Create sidebar
        self.side_frame = ttk.Frame(root, width=100, height=self.board_size)
        self.side_frame.grid(row=0, column=0)

        self.white_player = GreedyAI()
        self.black_player = RandomAI()

        self.white_label = ttk.Label(self.side_frame, text=self.white_player.name)
        self.white_label.pack()

        ttk.Label(self.side_frame, text="vs").pack()

        self.black_label = ttk.Label(self.side_frame, text=self.black_player.name)
        self.black_label.pack()

        simulate_btn = ttk.Button(self.side_frame, text="Play!", command=self.run_simulation)
        simulate_btn.pack()

        reset_btn = ttk.Button(self.side_frame, text="Reset", command=self.reset_board)
        reset_btn.pack()

        self.outcome_label = ttk.Label(self.side_frame, text="")
        self.outcome_label.pack()

        # Create bottombar
        self.bottom_frame = ttk.Frame(root, width=self.board_size + 100, height=300)
        self.bottom_frame.grid(row=1, column=0, columnspan=2)

        # Initialize chessboard
        self.board = chess.Board()
        self.highlighted_square = -1

        self.draw_chessboard()

    def handle_click(self, event):
        # Calculate the row and column from the click event
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)

        # Get the square from the row and column
        square = chess.square(col, row)
        print("Clicked", square)

        # Highlight the clicked square
        self.highlighted_square = square
        self.draw_chessboard()

    def update_board(self, new_board):
        self.board = new_board
        self.draw_chessboard()

    def get_board(self):
        return self.board

    def draw_chessboard(self):
        # Create SVG representation of the current chessboard position
        last_move = self.board.peek() if len(self.board.move_stack) > 0 else None
        squares = [self.highlighted_square] if self.highlighted_square != -1 else None
        svg_data = chess.svg.board(board=self.board, lastmove=last_move, squares=squares)
        # Convert SVG data to a PNG image using cairosvg
        png_data = cairosvg.svg2png(bytestring=svg_data)

        # Remove old board
        for widget in self.chessboard_frame.winfo_children():
            widget.destroy()

        # Create a Tkinter PhotoImage from the PNG data
        img = Image.open(io.BytesIO(png_data))
        img = ImageTk.PhotoImage(img)

        # Display the chessboard image in a Tkinter Label
        label = tk.Label(self.chessboard_frame, image=img)
        label.photo = img  # To prevent garbage collection
        label.grid(row=0, column=0)
      
        # Bind click events to chessboard
        # label.bind("<Button-1>", self.handle_click)

    def reset_board(self):
        self.board.reset()
        self.draw_chessboard()

    def run_simulation(self):
        if self.board.is_game_over():
            self.reset_board()
        self.outcome_label.configure(text="")
        self.play()

    def get_player(self):
        return self.white_player if self.board.turn == chess.WHITE else self.black_player
    
    def get_color_str(self):
        return "White" if self.board.turn == chess.WHITE else "Black"
      
    def play(self):
        if not self.board.is_game_over():
            move = self.get_player().make_move(self.board)

            if move not in self.board.legal_moves:
                print("Illegal Move by", self.get_player().name, move)
                return
            
            self.board.push(move)
            self.draw_chessboard()
            
            self.root.after(1, self.play)
        else:
            print("Outcome", self.board.outcome().result())
            self.outcome_label.configure(text=self.board.outcome().result())
            self.draw_chessboard()
    

        
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
