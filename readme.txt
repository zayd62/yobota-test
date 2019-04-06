How I approached the problem

I decided to split the program into multiple parts

1. file validation: error codes 5-9 were able to be checked before counters were inserted into the board
   the function 'validate_file()' is responsible for it
   error code 3 has two conditions: a game file with just a config, not game history
2. win checking: once a counter was inserted, the function 'find_winner()' is responsible for finding a winner
   it checks in multiple directions. more details in the docstring of 'find_winner()'
   it also completes the other half of error code 3:

   The file conforms to the format and contains only legal moves, but
   the game is neither won nor drawn by either player and there are
   remaining available moves in the frame

What I found easy

1. I found splitting the problem into smaller problems and working on those smaller problems made creating a solution
   much easier

What I found Challenging

1. In university, I was using Java and Web technologies and when debugging, I found myself remembering Python specific
   'features' such as a negative list index position means that it selects index positions from the end of the list

What I would like to improve

1. i think for very large board config (X, Y, Z) with very large values (guessing >10,000), the script will take a
   very long time and consume lots of memory so benchmark with very large numbers and try to improve performance
   Some improvements I can think of:

   - use multiprocessing module to take advantage of multiple CPU cores for the win validation functions as they can
     be executed in any order (file validation cannot as they depend on each other)
   - libraries such as Cython for performance improvements
   - native python C extensions
