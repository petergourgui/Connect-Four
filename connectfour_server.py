# Polling protocol implementation
from collections import namedtuple
import socket
import connectfour
import connectfour_main


GameConnection = namedtuple('GameConnection', ['socket', 'input', 'output'])


class ConnectFourProtocolError(Exception):
    pass


def connect(host: str, port: int) -> GameConnection:
    '''
    Connects to a Connect Four server on the given host and  port, returning 
    a GameConnection object describing that connection if successful, 
    or raising an exception if the attempt to connect fails.
    '''
    connectfour_socket = socket.socket()
    connectfour_socket.connect((host, port))
    connectfour_input = connectfour_socket.makefile('r')
    connectfour_output = connectfour_socket.makefile('w')

    return GameConnection(connectfour_socket, connectfour_input, connectfour_output)


def hello(game_connection: GameConnection, username: str) -> bool:
    '''
    Logs a user into the Connect Four server over a previously-made connection.
    Returns True if the user successfully logged in, False if the user was not
    able to log in.
    '''
    send_request(game_connection, f'I32CFSP_HELLO {username}')
    response = read_response(game_connection)

    if response == f'WELCOME {username}':
        return True
    else:
        return False


def close(game_connection: GameConnection) -> None:
    'Closes the connection to the Connect Four server.'
    game_connection.input.close()
    game_connection.output.close()
    game_connection.socket.close()


def create_game(game_connection: GameConnection) -> connectfour.GameState:
    '''
    Asks the user for the number of columns and rows, and creates a new game according to 
    their input. Also communicates to the server the number of columns and rows for the 
    new game. Returns a GameState if game was created successfully, returns None otherwise.
    '''
    try:
        num_columns, num_rows = connectfour_main.get_row_col()
        new_game = connectfour_main.game_setup(num_columns, num_rows)
        send_request(game_connection, f"AI_GAME {num_columns} {num_rows}")
        expect_response(game_connection, "READY")
        return new_game
    except:
        print("Unable to create a new game!")
        close(game_connection)
        return None


def send_request(game_connection: GameConnection, line: str) -> None:
    '''
    Writes a line of text to the server, including the appropriate 
    newline sequence, and ensures that it is sent immediately
    '''
    game_connection.output.write(line + '\r\n')
    game_connection.output.flush()
    

def read_response(game_connection: GameConnection) -> str:
    '''
    Reads a line of text sent from the server and returns it without
    a newline on the end of it.
    '''
    return game_connection.input.readline()[:-1]


def expect_response(game_connection: GameConnection, expected: str) -> None:
    '''
    Reads a line of text sent from the server, expecting it to contain
    a particular text. If the line of text received is different, this
    function raises an exception; otherwise, the function has no effect.
    '''
    line = read_response(game_connection)
    if line != expected:
        raise ConnectFourProtocolError()

