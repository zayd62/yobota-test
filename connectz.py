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


# end of class "ConnectBoard"

if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
