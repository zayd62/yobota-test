"""
This module is for the game Connect Z which is the same as Connect 4 but you can have a board of any size and require
any number of counters to win
"""
import sys


class ConnectBoard:
    """
    class for the game Connect 4 but for a board of any size and any number of counters to win. Reads a file that
    defines a board size and a play history

    Simulates the play history and calculate a winner as well as


    Args:
        path (str): path to game history file
    """

    def __init__(self, path):

        self.path = path
        self.config = []  # has the board config.
        self.history = []  # has the game history
        self.board = []  # stores the board as a nested list
        self.winner = ""  # stores the winner

    def generate_board(self):
        row = [0] * self.config[0]
        for i in range(0, self.config[1]):
            self.board.append(row)

    # below are miscellaneous helper methods used either on their own or in other methods

    @staticmethod
    def print_output_code(code):
        """
        This function is responsible for printing the output code

        Args:
            code (int): the output code to print
        """
        print(code)
        sys.exit(0)

    def extract_data_from_file(self):
        """
        Extracts the config data as well as the game history. Makes no assumptions on the validity of the game
        """
        with open(self.path, 'r') as file:
            # code to extract the config and store as a list
            self.config = file.readline().split(" ")

            # code to extract the game history and store as a list
            for i in file:
                self.history.append(i)

    def convert_to_int(self):
        """
        When reading from a file, python reads it as a string but we need them as ints.
        Since we store as lists, we need to convert into list

        We can only convert the data in the file to an int only if the file is validated as well as the format
        """
        temp = [int(i) for i in self.config]
        self.config = temp
        temp = [int(j) for j in self.history]
        self.history = temp

    def validate_file(self):
        """
        Checks to see if the path is a file that exists

        Returns:
            bool: true if file was loaded successfully, false if file not found
        """
        try:
            with open(self.path, 'r'):
                return True
        except FileNotFoundError:
            return False

    # below are all the validation helper methods that are run before the game history is simulated

    def validate_file_format(self):
        """
        This validates the file to make sure it is in the correct format according to the specification.
        It validates the config

        A valid format looks like the following:

        `1 2 3` where
        - 1: width of the board (column)
        - 2: height of the board (row)
        - 3: length of line (vertical, horizontal or diagonal) needed to win

        Returns:
            bool: true if file follows the format, false if it does not
        """

        if len(self.config) == 3:
            return True
        else:
            return False

    def validate_legal_game(self):
        """
        checks to make sure that the game is legal.

        A legal game is one where you can get the counters in a row.

        - file with `3 3 4` is illegal as in a 3x3 board, you cant get 4 in a row
        - file with `7 7 4` is legal as in a 7x7 board, you can get 4 in a row

        This assumes that the file is in the valid format

        Returns:
            bool: True if the game can be won. false otherwise
        """
        # to see if the game is valid a "line" of the same type needs to be formed
        # it can be formed horizontally, vertically and diagonally
        # as long as a "line" can be formed at least once, a game is "legal"
        # so check if either first_line_int[0] or first_line_int[1] >= first_line_int[2] to be valid

        if self.config[0] >= self.config[2] or self.config[1] >= self.config[2]:
            return True
        else:
            return False

    def validate_legal_column(self):
        """
        Checks the file to see if they are any illegal columns

        An illegal column is when you are trying to put a counter into a column that does not exist

        For example, for a legal game with specification `3 4 3`, if there is a move `5`, then this is an illegal column
        as you are trying to insert into column 5 when there is only 3 columns

        Assumes that the game is legal;

        Returns:
            bool: True if all the columns are legal, False otherwise
        """

        for i in self.history:
            if i > self.config[0]:
                return False
        return True

    def validate_legal_row(self):
        """
        Checks the file to see if there are any illegal rows

        An illegal row is when a column is full and you are trying to insert it into that column.

        Works by keeping track of the number of times a move appears and if a move exceeds the number of rows,
        the function  will then return false

        Assumes that the columns are legal

        Returns:
            bool: true if the rows are legal, false otherwise
        """
        row_track = [0] * (self.config[0] + 1)
        for i in self.history:
            row_track[i] += 1
            if row_track[i] > self.config[0]:
                return False
        return True

    def no_history(self):
        """
        If the file has no game history and just a config, then it is considered incomplete

        Returns:
            bool: True if there is no history, false otherwise
        """
        if len(self.history) == 0:
            return False
        else:
            return True


# end of class "Connect Board"

def main():
    """
    This function is ran if the file is executed as a script. If imported, this will not run
    """
    if len(sys.argv) != 2:
        print("Provide one input file")
        sys.exit(0)
    else:
        board = ConnectBoard(sys.argv[1])

        if not board.validate_file():
            board.print_output_code(9)

        board.extract_data_from_file()

        if not board.validate_file_format():
            board.print_output_code(8)

        board.convert_to_int()

        if not board.validate_legal_game():
            board.print_output_code(7)

        if not board.validate_legal_column():
            board.print_output_code(6)

        if not board.validate_legal_row():
            board.print_output_code(5)

        # check if there is a game history
        if not board.no_history():
            board.print_output_code(3)

        # all validation checks are complete.

        # build the board based on the config
        board.generate_board()



if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
