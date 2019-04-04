#!/usr/bin/env bash
echo testing no command line arguments, expected value: Provide one input file, obtained
python connectz.py
echo testing file error, expected value: 9, obtained
python connectz.py yobotaTests/file.txt
echo testing invalid file, expected value: 8, obtained
python connectz.py yobotaTests/invalid_file.txt
echo testing illegal game, expected value: 7, obtained
python connectz.py yobotaTests/illegal_game.txt
echo testing illegal column, expected value: 6, obtained
python connectz.py yobotaTests/illegal_column.txt
echo testing illegal row, expected value: 5, obtained
python connectz.py yobotaTests/illegal_row.txt
echo testing only dimension lines, expected 3, obtained
python connectz.py only_dimensions.txt