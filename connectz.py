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
        open(path, 'r')
        return True

    except FileNotFoundError:
        return False


def validate_file_format(path):
    """
    This validates the file to make sure it is in the correct format according to the specification

    A valid format looks like the following:

    ``1 2 3``

    Args:
        path (str): path to the game file

    Returns:
        bool: true if file follows the format, false if it does not
    """

    file = open(path, 'r')
    first_line = file.readline().split(" ")

    if len(first_line) == 3:
        return True
    else:
        return False


def print_output_code(code):
    """
    This function is responsible for printing the output code

    Args:
        code (str): the output code to print
    """
    print(code)
    sys.exit(0)


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

    # now to validate the input file
    if not validate_file_format(sys.argv[1]):
        print_output_code("8")
    else:
        print("valid")


if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
