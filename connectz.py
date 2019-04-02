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
if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
