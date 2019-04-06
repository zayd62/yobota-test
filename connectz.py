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

        self.path = path  # path to the game file
        self.config = []  # has the board config.
        self.history = []  # has the game history
        self.board = []  # stores the board as a nested list
        self.player_one_move = True

    def generate_empty_board(self):
        """
        creates the connect board using the dimensions in self.config
        """
        row = [0] * self.config[0]
        for i in range(0, self.config[1]):
            self.board.append(row[:])

    def insert_into_board(self, value, column):
        """
        Inserts a "counter" into the board. The "counter" is the player number (either one or two) and is based on
        the parameter ``value``. Since lists start at index position 0 and column numbers start at 1, all column
        numbers will be subtracted by 1. We only insert into a column where there is a zero

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
                self.find_winner(column - 1, i)  # stores the result of the win check
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
        """
        Given a position within the board, it finds a winner. Uses self.win_check() to find winner and
        print the appropriate output code

        Args:
            column (int): the column number
            row (int): the row number
        """
        # Since there are multiple directions to win a game, all directions are checked and inserted into a list
        results = []

        results.append(self.win_check(column, row, -1, 0))  # for horizontal left
        results.append(self.win_check(column, row, 1, 0))  # for horizontal right
        results.append(self.win_check(column, row, 0, 1))  # for vertical down
        results.append(self.win_check(column, row, 1, -1))  # for diagonal upper right
        results.append(self.win_check(column, row, -1, -1))  # for diagonal upper left
        results.append(self.win_check(column, row, 1, 1))  # for diagonal lower right
        results.append(self.win_check(column, row, -1, 1))  # for diagonal lower left

        # if true, player 1 won
        if 1 in results:
            if self.illegal_continue_check():
                self.print_output_code(1)
            else:
                self.print_output_code(4)

        # if true, player 2 won
        elif 2 in results:
            if self.illegal_continue_check():
                self.print_output_code(2)
            else:
                self.print_output_code(4)

        # neither player 1 or 2 won with this move
        else:
            pass

    def illegal_continue_check(self):
        """
        This function checks if there is an illegal continue

        An illegal continue is one where after a winner is found, another move is made

        Returns:
            bool: True if there is an illegal continue, false otherwise

        """

        # as we insert moves into the board, the move played is overwritten by a zero in self.history.
        # a zero is only written if there is no winner.
        # if a winner is detected, then the winning move is not written over so the code below rewrites the
        # winning move with a zero
        for i in range(0, len(self.history)):
            if self.history[i] != 0:
                self.history[i] = 0
                break

        # i is the index position of the winning move
        # if there are any moves after this, then moves have been made after a game has been won which illegal

        # use list slicing to get all the elements after the winning move (not including the winning move).
        # we do i + 1 as index i is the winning move
        # if there are elements in the sliced list, then illegal moves have been made
        if len(self.history[(i + 1):]) == 0:
            return True
        else:
            return False

    # below are all the win checking helper functions

    def win_check(self, column_start_point, row_start_point, column_offset, row_offset):
        """
        This function given a starting point in the board will attempt to find a winner by checking the the cells
        determined by the offset

        The offset determines which direction the program will move across the board to find the next counter. The
        number of counters checked is determined by self.config[2] which states the number of counters needed for a win

        Below is a table of the different directions to check for a win:

         ====================== ==================================== =============== ============
                Win Type                    Description               Column Offset   Row Offset
         ====================== ==================================== =============== ============
          Horizontal Left        Move one to the left                 -1              0
          Horizontal Right       Move one to the right                +1              0
          Vertical Down          Move one down                        0               +1
          Diagonal Upper Right   Move one to the right and one up     +1              -1
          Diagonal Upper Left    Move one to the left and one up      -1              -1
          Diagonal Lower Right   Move one to the right and one down   +1              +1
          Diagonal Lower Left    Move one to the left and one up      -1              +1
         ====================== ==================================== =============== ============

        Note: we dont check Vertical Up as that would mean that a counter is inserted underneath another counter which
        is not possible

        Args:
            column_start_point (int): the column number where the program will start
            row_start_point (int): the row number where the program will start
            column_offset (int): the number of rows the program will move to find the next counter to check
            row_offset (int): the number of rows the program will move to find the next counter to check

        Returns:
            int: If player one inserted a winning move, then a 1 is returned, 2 is returned for player two and 0 if
            there are no winners
        """

        # determine which player inserted a counter. The board stores which player inserted a counter
        if self.player_one_move:
            number_to_find = 1
        else:
            number_to_find = 2

        # looks through the board which is a nested list
        # depending on the offset, the offset may ask to check a cell that does not exist.
        # e.g for config ``7 7 4`` the cell ``8,8`` does not exist and trying to check that cell will throw an index
        # error. The offset may also produce negative numbers, negative numbers are valid index position in lists
        # and are interpreted as starting from the end of the list but in our situation, a negative value eg; ``-1,2``
        # is checking a cell that does not exist. For all the conditions mentioned above, we return a 0 which means
        # 'no winnner'
        try:
            for i in range(0, self.config[2]):
                if column_start_point < 0 or row_start_point < 0:
                    return 0
                if self.board[row_start_point][column_start_point] == number_to_find:
                    # modifying the start points so that it checks the next cell
                    # the cell checked next is determined by the offset
                    column_start_point += column_offset
                    row_start_point += row_offset
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

        # if config contains an element that is a string, error code 8 should print
        try:
            temp = [int(i) for i in self.config]
            self.config = temp
        except ValueError:
            self.print_output_code(8)

        # if any of the moves are a non-int, error code 7
        try:
            temp = [int(j) for j in self.history]
            self.history = temp
        except ValueError:
            self.print_output_code(7)


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
        board.generate_empty_board()

        # for i in board.history:
        for i in range(0, len(board.history)):
            if board.player_one_move:
                board.insert_into_board(1, board.history[i])
            else:
                board.insert_into_board(2, board.history[i])

            # this changes the player move. true is player 1, false is player 2
            board.player_one_move = not board.player_one_move

            # if the insertion is not a winning move, you set the history to 0 to mark it as 'inserted'
            # if the last move in the history is the winning move, they board.history[last_element] != 0
            board.history[i] = 0

        # if program reaches here, then there are no winners
        # only two things can happen

        # incomplete: there are no winners and there are still spaces left in the board
        # draw: there are no winners and the board is full

        # goes through board and tries to find any '0's' if found, then the game can continue
        for i in board.board:
            if 0 in i:
                board.print_output_code(3)

        # no winners and no zeros therefore board is full and it is a draw
        board.print_output_code(0)


if __name__ == '__main__':
    # file is being run directly not as an imported module
    main()
