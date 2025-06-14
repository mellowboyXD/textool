#!/bin/python3.13

from enum import Enum
import sys
from typing import Iterator

options = {
    "-f": "--freq",
    "-u": "--unique",
    "-l": "--lengths"
}

class Options(Enum):
    FREQ = 0
    UNIQ = 1
    LEN = 2

class UsageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = f"ERROR: {message}"


    def error_and_exit(self):
        print(f"ERROR: {self.message}")
        print(f"Options: {long_options}")
        exit()

short_options = list(options.keys())
long_options = list(options.values())

class WordStream:
    def __init__(self, line):
        print(f"Current line: {line.split()}")

    def __iter__():
        pass

    def __next__():
        pass

def read_file(path: str) -> Iterator[str]:
    try:
        with open(path, "r") as file:
            for line in file:
                _ = line.encode("utf-8")
                yield line
    except FileNotFoundError:
        print(f"ERROR: File '{path}' not found.")
        raise IOError
    except IsADirectoryError:
        print(f"ERROR: '{path}' is a directory.")
        raise IOError
    except UnicodeDecodeError:
        print(f"ERROR: Could not decode '{path}'.")
        raise IOError


def main(*args) -> None:
    argc = len(args)
    try:
        if argc < 1:
            raise UsageError("Not enough arguments")
    except UsageError as err:
        err.error_and_exit()

    # Handle args
    opts = set()
    fileName = ""
    error_invalid_flag = False
    for c in args:
        if c in short_options:
            opts.add(Options(short_options.index(c)))
        elif c in long_options:
            opts.add(Options(short_options.index(c))) 
        elif c[0] != "-":
            fileName = c
        else:
            error_invalid_flag = True

    # User types a command that is not valid
    try:
        if error_invalid_flag:
            raise UsageError("Invalid command.")
    except UsageError as err:
        err.error_and_exit()

    # User does not provide file name
    try: 
        if not fileName:
            raise UsageError("File input not provided")
    except UsageError as err:
        err.error_and_exit()

    try:
        for line in read_file(fileName):
            stream = WordStream(line)
    except IOError:
        exit()

if __name__ == "__main__":
    main(*sys.argv[1:])
