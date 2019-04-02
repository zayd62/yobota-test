import sys


class ConnectBoard:
    """
    class for the game Connect 4 but for a board of any size and any number of counters to win
    """

    def __init__(self, path):
        """
        
        Args:
            path (str): path to game history file
        """

        self.path = path


# end of class "Connect Board"

def load_text_file(path):
    """
    Loads file from path

    Args:
        path (str): the path to the text file

    Returns:
        bool: true if file was loaded successfully, false if file not found
    """
    try:
        with open(path, 'r') as file:
            return True

    except FileNotFoundError:
        return False


def validate_file_format(path):
    """
    This validates the file to make sure it is in the correct format according to the specification

    A valid format looks like the following:

    `1 2 3` where
    - 1: width of the board (column)
    - 2: height of the board (row)
    - 3: length of line (vertical, horizontal or diagonal) needed to win

    Args:
        path (str): path to the game file

    Returns:
        bool: true if file follows the format, false if it does not
    """

    config = extract_config(path)

    if len(config) == 3:
        return True
    else:
        return False


def legal_game(path):
    """
    checks to make sure that the game is legal.

    A legal game is one where you can get the counters in a row.

    - file with `3 3 4` is illegal as in a 3x3 board, you cant get 4 in a row
    - file with `7 7 4` is legal as in a 7x7 board, you can get 4 in a row

    This assumes that the file is in the valid format

    Args:
        path (str): path to game file

    Returns:
        bool: True if the game can be won. false otherwise
    """
    config = extract_config(path)

    # first_line is a list of numbers of type string so convert to integers
    first_line_int = [int(i) for i in config]

    # to see if the game is valid a "line" of the same type needs to be formed
    # it can be formed horizontally, vertically and diagonally
    # as long as a "line" can be formed at least once, a game is "legal"
    # so check if either first_line_int[0] or first_line_int[1] >= first_line_int[2] to be vali

    if first_line_int[0] >= first_line_int[2] or first_line_int[1] >= first_line_int[2]:
        return True
    else:
        return False


def legal_column(path):
    """
    Checks the file to see if they are any illegal columns

    An illegal column is when you are trying to put a counter into a column that does not exist

    For example, for a legal game with specification `3 4 3`, if there is a move `5`, then this is an illegal column as
    you are trying to insert into column 5 when there is only 3 columns

    Assumes that the game is leha;

    Args:
        path (str): path to the text file

    Returns:
        bool: True if all the columns are legal, False otherwise
    """
    pass


# helper functions, any code that is used multiple times will be converted into a function
def print_output_code(code):
    """
    This function is responsible for printing the output code

    Args:
        code (str): the output code to print
    """
    print(code)
    sys.exit(0)


def extract_config(path):
    """
    Helper function used to extract the config from a text file
    
    This does not do any validation of the config, it simply just extracts the first line
    Args:
        path (str): the path to the game config 

    Returns:
        List[str]: an string array with the config.
    """
    with open(path, 'r') as file:
        return file.readline().split(" ")


def main():
    """
    Function that is called if file 'connectz.py' is being run directly.

    This function processes an input file and creates a 'Connect z' board and checks the game to see if it is a valid
    game or not
    """

    # 'sys.argv' is a list which contains the file name in sys.argv[0] and command line arguments in each index position
    # we need to check make sure that only one command line argument is passed, the game file so len(sys.argv != 2) == 2
    # otherwise we print message stating to provide one input file

    if len(sys.argv) != 2:
        print("Provide one input file")
        sys.exit(0)

    # now attempt to load file. function returns a boolean. if false, then file does not exist
    if not load_text_file(sys.argv[1]):
        print_output_code("9")

    # now to validate the input file, if false, file is in invalid format
    if not validate_file_format(sys.argv[1]):
        print_output_code("8")

    # now to check if the game is legal. i.e. the game can be won.
    if not legal_game(sys.argv[1]):
        print_output_code("7")

    # check to see if there are any illegal column
    if not legal_column(sys.argv[1]):
        print_output_code("6")

    # once all the checks have passed, you can then


if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
