Connect4 Multiplayer (Online & Shell)

This project is a Python-based implementation of Connect Four, a two-player connection game where the goal is to be the first to form a vertical, horizontal, or diagonal 
line of four of your pieces. The game includes both local shell play and online play where you can connect to a server for multiplayer action.

Key Features:
Local Shell Play: Play the game offline against a friend locally in the terminal.
Online Play: Connect to a server to play against an AI or other players.
Flexible Board Sizes: You can specify the number of rows and columns (minimum 4, maximum 20).
Valid Moves & Winner Detection: Handles invalid moves and automatically detects the winner.


To play the shell version of the game locally, simply run connectfour_shell.py
Follow the on-screen prompts to specify the board size and make your moves

To play the online version of the game through a server, simply run connectfour_online.py
You will be asked for:
Host: The server's address
Port: The port on which the server is listening
Username: Your player username
The game will then be created on the server. Play your turns by choosing to "drop" or "pop" pieces and selecting columns.

Game Controls:
D, followed by space, followed by column number to drop in.
P, followed by space, followed by column number to pop from the bottom.