import connectfour
import connectfour_main


def run_shell_game() -> None:
    'Creates and runs a game until there is a winner'
    print("Welcome to the local shell version of Connect Four!")
    current_game = None
    while True:
        try:
            num_columns, num_rows = connectfour_main.get_row_col()
            current_game = connectfour_main.game_setup(num_columns, num_rows)
            break
        except:
            print("Invalid input. Please try again!")

    
    game_over = False
    while not game_over:
        connectfour_main.print_board(current_game)
        connectfour_main.print_turn(current_game)
        try:
            player_move, player_column = connectfour_main.get_move()
            current_game = connectfour_main.play_turn(current_game, player_move, player_column)
        except connectfour.InvalidMoveError:
            print("Invalid move was made.")
        except connectfour.GameOverError:
            print("Unable to make move, the game is over.")
        except ValueError:
            print("Invalid move was made.")
        except:
            print("Invalid input.")

        if connectfour.winner(current_game) != connectfour.EMPTY:
            connectfour_main.print_board(current_game)
            connectfour_main.print_winner(current_game)
            game_over = True


if __name__ == '__main__':
    run_shell_game()
