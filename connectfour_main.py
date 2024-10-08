import connectfour


def game_setup(num_columns: int, num_rows: int) -> connectfour.GameState:
    'Sets up a game of Connect Four with the given number of rows and columns.'
    current_game = connectfour.new_game(num_columns, num_rows)
    return current_game


def get_row_col() -> (int, int):
    'Asks the user for the number of rows and columns they want for their game and returns their input'
    while True:
        row_and_col = input("Enter the number of rows and then columns separated by spaces (Minimum 4 and Maximum 20): ")
        row_and_col = row_and_col.strip()
        row_and_col = row_and_col.split()
        row = int(row_and_col[0])
        col = int(row_and_col[1])

        return col, row
        

def print_board(current_game: connectfour.GameState) -> None:
    "Prints the current state of the Connect Four board."
    for i in range(len(current_game.board)):
        column_number = i + 1
        if column_number >= 9:
            print(column_number, '', end = '')
        else:
            print(column_number, ' ', end = '')
    print()

    for row_num in range(len(current_game.board[0])):
        for col_num in range(len(current_game.board)):
            element = current_game.board[col_num][row_num]
            if element == connectfour.YELLOW:
                print('Y  ', end='')
            elif element == connectfour.RED:
                print('R  ', end='')
            else:
                print(".  ", end='')
        print()


def print_winner(current_game: connectfour.GameState) -> None:
    'Prints the winner if there is a winner.'
    if connectfour.winner(current_game) == connectfour.RED:
        print("Red is the winner!")
    elif connectfour.winner(current_game) == connectfour.YELLOW:
        print("Yellow is the winner!")


def print_turn(current_game: connectfour.GameState) -> None:
    "Prints which player's turn it is."
    if current_game.turn == connectfour.RED:
        print("Red's turn")
    else:
        print("Yellow's turn")
        

def play_turn(current_game: connectfour.GameState, player_move: str, player_column: int) -> connectfour.GameState:
    '''
    Makes a move based on the given move and column. Returns an updated GameState if 
    the move was valid, otherwise returns the same GameState.
    '''
    if player_move == 'D':
        current_game = connectfour.drop(current_game, player_column - 1)
        
    elif player_move == 'P':
        current_game = connectfour.pop(current_game, player_column - 1)

    return current_game


def get_move() -> (str, int):
    'Asks the user if they want to drop or pop for their next move and which column. Returns their input.'
    while True:
        player_move = input("Enter your move (D for Drop, P for Pop) followed by a space and column number: ")
        player_move = player_move.strip()
        player_move = player_move.split()
        action = player_move[0]
        column_number = int(player_move[1])

        return action, column_number