import connectfour_main
import connectfour_server
import connectfour


def play_online_connectfour() -> None:
    '''
    Creates and runs an online game until there is a winner or closes the connection
    and ends the program if the protocol is not followed.
    '''
    game_connection = _login()
    if game_connection == None:
        return
    current_game = connectfour_server.create_game(game_connection)
    if current_game == None:
        return
    
    game_over = False
    while not game_over:
        connectfour_main.print_board(current_game)
        print()
        connectfour_main.print_turn(current_game)

        current_game = _make_move_online(game_connection, current_game)
        if current_game == None:
            game_over = True
            connectfour_server.close(game_connection)


def _make_move_online(game_connection: connectfour_server.GameConnection, current_game: connectfour.GameState) -> None:
    '''
    Sends the move that was made on the Connect Four server and receives the AI's move.
    Returns an updated GameState if the server output is "READY". If there is a winner or 
    an invalid input, None is returned.
    '''
    while True:
        try:
            player_move, player_column = connectfour_main.get_move()
        except:
            print("Invalid input!")
            return None
        if _is_valid_input(player_move, player_column):
            _send_move(game_connection, player_move, player_column)
            try:
                current_game = connectfour_main.play_turn(current_game, player_move, player_column)
                break
            except:
                print("Inavlid move. Please try again!")
                connectfour_server.expect_response(game_connection, 'INVALID')
                connectfour_server.expect_response(game_connection, 'READY')
                continue
        else:
            print("Invalid input!")
            return None


    while True:
        response = connectfour_server.read_response(game_connection)
        if response == 'INVALID':
            print("Invalid move. Please try again!")
            connectfour_server.expect_response(game_connection, 'READY')
            continue

        if response.startswith('OKAY'):
            connectfour_main.print_board(current_game)
            print()
            connectfour_main.print_turn(current_game)
            continue

        if response.startswith('READY'):
            return current_game

        if response.startswith('DROP') or response.startswith('POP'):
            ai_play = response.split()
            ai_move = ai_play[0]
            ai_column = int(ai_play[1])
            if ai_move == 'DROP':
                ai_move = 'D'
            else:
                ai_move = 'P'
            if _is_valid_input(ai_move, ai_column):
                try:
                    current_game = connectfour_main.play_turn(current_game, ai_move, ai_column)
                    continue
                except:
                    print("Server sent an invalid move!")
                    print(ai_move, ai_column)
                    return None
            else:
                print("Server sent an invalid input!")
                return None
        
        if response.startswith('WINNER'):
            connectfour_main.print_board(current_game)
            print()
            connectfour_main.print_winner(current_game)
            return None
        

def _is_valid_input(player_move: str, player_column: int) -> bool:
    'Returns True if the given input and column are valid. False otherwise.'
    if player_move == 'D' or player_move == 'P':
        if type(player_column) == int:
            return True
    return False
            

def _send_move(game_connection: connectfour_server.GameConnection, player_move: str, player_column: int) -> None:
    "Sends the user's move to the server."
    if player_move == 'D':
        connectfour_server.send_request(game_connection, f"DROP {player_column}")
    if player_move == 'P':
        connectfour_server.send_request(game_connection, f"POP {player_column}")


def _login() -> connectfour_server.GameConnection:
    '''
    Attempts to connect the user's specified host and port, and sends a hello message 
    according to the Connect Four server protocol. Returns a GameConnetion if the 
    connection is successful, returns None otherwise.
    '''
    game_connection = None
    try:
        host = _get_host()
        port = _get_port()
        game_connection = connectfour_server.connect(host, port)
    except:
        print("Unable to connect to server!")
        return None
    
    username = _get_username()
    connected = connectfour_server.hello(game_connection, username)
    if connected:
        return game_connection
    else:
        print("Invalid username!")
        connectfour_server.close(game_connection)
        return None


def _get_host() -> str:
    '''
    Asks the user for the host where a Connect Four server is running and
    returns their input.
    '''
    host = input("Enter the host where you would like to play Connect Four: ")
    return host


def _get_port() -> str:
    'Asks the user for the port on which the Connect Four server is listening'
    port = int(input("Enter the port on which the Connect Four server is listening: "))
    return port


def _get_username() -> str:
    'Asks the user for a username'
    username = input("Enter your username (No whitespace characters allowed): ")
    return username


if __name__ == '__main__':
    play_online_connectfour()
