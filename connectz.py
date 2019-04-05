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
        self.player_one_move = True

    def generate_board(self):
        """
        creates the connect board using the dimensions
        """
        row = [0] * self.config[0]
        for i in range(0, self.config[1]):
            self.board.append(row[:])

    def insert_into_board(self, value, column):
        """
        Inserts a "counter" into the board. The "counter" is the player number (either one or two) and is based on value
        Since lists start at index position 0 and column numbers start at 1, all column numbers will automatically be
        subtracted by 1. We only insert into a colun where there is a zero

        No checks for inserting into a row that does not exist as that should have been validated already and will
        throw an error

        Args:
            value (int): the value to be used as the "counter". usually a 1 or 2
            column (int): the column number a "counter" is inserted into.
        """

        # to get a value in a position, we do self,board[row][column]
        # we need to insert into a column from the bottom up so we need to loop through all the rows where
        # the number of rows is self.config[0]
        # to obtain the column we use the "column" argument
        # to get the value in a column position, we do self.board[i][column]
        # i is defined below in the for loop and represents the row
        # we start from the bottom row which is the maximum number of rows (subtract 1 as list index start at 0)
        # finish at 0 which will give us the top row. and step through "-1" times so we go through each row
        for i in range(self.config[0] - 1, -1, -1):
            if self.board[i][column - 1] == 0:
                self.board[i][column - 1] = value
                result = self.find_winner(column - 1, i)  # stores the result of the win check
                return

    def validate_file(self):
        """
        A wrapper function that calls all the helper validation methods and if any of the validation methods fail
        the appropriate output code will be printed to terminal
        """
        # check if game history file exists
        if not self.validate_file_existence():
            self.print_output_code(9)

        # extract the data from file and store in ConnectBoard object
        self.extract_data_from_file()

        # check if the config is valid
        if not self.validate_config():
            self.print_output_code(8)

        # convert data from string to int
        self.convert_to_int()

        # checks if the game can actually be won
        if not self.validate_legal_game():
            self.print_output_code(7)

        # checks if the columns are valid
        if not self.validate_legal_column():
            self.print_output_code(6)

        # checks if the rows are valid
        if not self.validate_legal_row():
            self.print_output_code(5)

        # check if there is a game history
        if not self.no_history():
            self.print_output_code(3)

    def find_winner(self, column, row):
        result_horizontal_left = self.win_horizontal_left(column, row)
        result_horizontal_right = self.win_horizontal_right(column, row)
        result_vertical_down = self.win_vertical_down(column, row)
        return [result_horizontal_left, result_horizontal_right, result_vertical_down]

    # below are all the win checking helper functions

    def win_horizontal_left(self, column, row):
        """
        This function given a column and a row, check to see if there is a solution in the horizontal left of from the
        starting point.


        A horizontal left victory looks like the following (starting from cell 4,7)::

            .---.---.---.---.---.---.---.
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
            '---'---'---'---'---'---'---'

        Args:
            column (int): the point in the column where you start looking
            row (int): the point in the row where you start looking

        Returns:
            int: player number of who won, 0 if no one won
        """

        # boolean self.player_one_move determines whose move it is, True is player 1, false is player 2
        if self.player_one_move:
            number_to_find = 1
        else:
            number_to_find = 2

        # self.config[2] determines the number of counters needed to win so we need to check that many times
        # assuming number_to_find = 1, we check for 1's, self.config[2] timesin horizontal left
        # if found, return True, false otherwise

        # we put it in a try-except because we may get an IndexError because we may access cells that do not exist
        # for the example in docstring, if we start a 1,7 and we need 4 to win, checking the second cell will be a cell
        # that does not exist which will then raise an IndexError. if this happens, we return false
        # as a win cannot happen

        # we also have ``column < 0`` because in python, a -1 list index starts from the end of the list but -1 means
        # checking a cell that does not exist in this example

        try:
            for i in range(0, self.config[2]):
                if column < 0:
                    return 0
                if self.board[row][column] == number_to_find:
                    column -= 1  # this will ensure that the cell of the left is checked next
                else:
                    return 0
            return number_to_find
        except IndexError:
            return 0

    def win_horizontal_right(self, column, row):
        """
        This function given a column and a row, check to see if there is a solution in the horizontal right of from the
        starting point.


        A horizontal right victory looks like the following (starting from cell 4,7)::

            .---.---.---.---.---.---.---.
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
            '---'---'---'---'---'---'---'

        Args:
            column (int): the point in the column where you start looking
            row (int): the point in the row where you start looking

        Returns:
            int: player number of who won, 0 if no one won
        """

        # boolean self.player_one_move determines whose move it is, True is player 1, false is player 2
        if self.player_one_move:
            number_to_find = 1
        else:
            number_to_find = 2

        # self.config[2] determines the number of counters needed to win so we need to check that many times
        # assuming number_to_find = 1, we check for 1's, self.config[2] times in horizontal right
        # if found, return True, false otherwise

        # we put it in a try-except because we may get an IndexError because we may access cells that do not exist
        # for the example in docstring, if we start a 1,7 and we need 4 to win, checking the second cell will be a cell
        # that does not exist which will then raise an IndexError. if this happens, we return false
        # as a win cannot happen

        # we also have ``column < 0`` because in python, a ``-1`` list index starts from the end of the list but ``-1``
        # means checking a cell that does not exist in this example

        try:
            for i in range(0, self.config[2]):
                if column < 0:
                    return 0
                if self.board[row][column] == number_to_find:
                    column += 1  # this will ensure that the cell of the right is checked next
                else:
                    return 0
            return number_to_find
        except IndexError:
            return 0

    def win_vertical_down(self, column, row):
        """
        This function given a column and a row, check to see if there is a solution in the vertical down from the
        starting point.


        A horizontal right victory looks like the following (starting from cell 4,4)::

            .---.---.---.---.---.---.---.
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
            :---+---+---+---+---+---+---:
            | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
            '---'---'---'---'---'---'---'

        Args:
            column (int): the point in the column where you start looking
            row (int): the point in the row where you start looking

        Returns:
            int: player number of who won, 0 if no one won
        """

        # boolean self.player_one_move determines whose move it is, True is player 1, false is player 2
        if self.player_one_move:
            number_to_find = 1
        else:
            number_to_find = 2

        # self.config[2] determines the number of counters needed to win so we need to check that many times
        # assuming number_to_find = 1, we check for 1's, self.config[2] times in horizontal right
        # if found, return True, false otherwise

        # we put it in a try-except because we may get an IndexError because we may access cells that do not exist
        # for the example in docstring, if we start a 1,7 and we need 4 to win, checking the second cell will be a cell
        # that does not exist which will then raise an IndexError. if this happens, we return false
        # as a win cannot happen

        # we also have ``column < 0`` because in python, a ``-1`` list index starts from the end of the list but ``-1``
        # means checking a cell that does not exist in this example

        try:
            for i in range(0, self.config[2]):
                if column < 0:
                    return 0
                if self.board[row][column] == number_to_find:
                    row += 1  # this will ensure that the below is checked next
                else:
                    return 0
            return number_to_find
        except IndexError:
            return 0

    # below are all the validation helper methods that are run before the game history is simulated

    def validate_file_existence(self):
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

    def validate_config(self):
        """
        This validates the file to make sure it is in the correct format according to the specification.
        It validates the config

        A valid format looks like the following:

        `1 2 3` where:

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
            bool: True if the game is legal. false otherwise
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
        Since we store the file data in lists, we need to convert all elements in the list from
        string to ints

        We can only convert the data in the file to an int only if the file is validated as well as the format

        Makes no assumption on the validity of the data
        """
        temp = [int(i) for i in self.config]
        self.config = temp
        temp = [int(j) for j in self.history]
        self.history = temp


# end of class "Connect Board"

def main():
    """
    This function is ran if the file is executed as a script. If imported, this will not run
    """

    # start of file validation

    # check if correct arguments are provided
    if len(sys.argv) != 2:
        print("Provide one input file")
        sys.exit(0)
    else:

        # create ConnectBoard object
        board = ConnectBoard(sys.argv[1])

        # validate the game file
        board.validate_file()

        # build the board based on the config
        board.generate_board()

        for i in board.history:
            if board.player_one_move:
                board.insert_into_board(1, i)
            else:
                board.insert_into_board(2, i)

            board.player_one_move = not board.player_one_move
        print("board built")


if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
