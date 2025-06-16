#!/bin/python3.13

import sys
from typing import Iterable, Iterator
from enum import Enum

cmd_options = {
    "-f": "--freq",
    "-u": "--unique",
    "-l": "--lengths"
}

class Options(Enum):
    FREQ = 0
    UNIQ = 1
    LEN = 2


short_options = list(cmd_options.keys())
long_options = list(cmd_options.values())

class Logger:
    def __init__(self):
        pass

    def Error(self, *message):
        print(f"[LOG ERROR]:")
        for msg in message:
            print(f"\t: {msg}")

    def Log(self, *message):
        print(f"[LOG]:")
        for msg in message:
            print(f"\t: {msg}")


class UsageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = f"ERROR: {message}"


    def error_and_exit(self):
        print(f"ERROR: {self.message}")
        print(f"Options: {long_options}")
        exit()


class InvalidFilter(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class WordStream:
    w = []
    def __init__(self, line):
        # the quick, brown fox jumps over the lazy dog.
        self.w = []
        for word in line.split():
            token = ""
            for letter in word:
                if letter.isalpha() or letter.isnumeric():
                    token += letter
                else:
                    if token:
                        self.w.append(token)
                    token = ""

            if token:
                self.w.append(token)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.w) == 0:
            raise StopIteration
        return self.w.pop(0)


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


# TODO: Count words
def count_words(ws: Iterable, *filters, case_sensitive=False, **kwargs) -> dict:
    """
    `ws` - Any iterable of words
    `*filters` - Are callables that filters for specific words
    `case_sensitive` - Toggles normalization
    `**kwargs` - May include `min_length`, `max_items`
    """
    for filter in filters:
        try:
            if not callable(filter):
                raise InvalidFilter("Filters must be callables")

            if not isinstance(filter("mellowboyXD"), bool):
                raise InvalidFilter("Filters take in `str` and returns `bool`")

        except InvalidFilter as err:
            Logger().Error(err.message, filter)
        except AttributeError as err:
            Logger().Error("Filters must take in `str` as parameter argument",
                           filter)

    options = kwargs.copy()
    max_items = -1
    min_length = -1
    max_length = -1
    for opts in kwargs.keys():
        if opts in options:
            match opts:
                case "max_length":
                    max_length = options.pop(opts)
                case "min_length":
                    min_length = options.pop(opts)
                case "max_items":
                    max_items = options.pop(opts)

    counter = {}
    for word in ws:
        word: str = word if case_sensitive else word.lower()

        skip = False
        for filter in filters:
            if not filter(word):
                skip = True
                break

        if skip:
            continue

        if min_length != -1 and len(word) < min_length:
            continue

        if max_length != -1 and len(word) > max_length:
            continue

        try:
            if options:
                raise InvalidFilter("Undefined Keyword Args")
        except InvalidFilter as err:
            Logger().Error(err.message)

        if word in counter:
            counter[word] += 1
        else:
            if len(counter) < max_items:
                counter[word] = 1
            elif max_items == -1:
                counter[word] = 1

    return counter


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
            # TODO: Implement Counting Here
    except IOError:
        exit()

if __name__ == "__main__":
    main(*sys.argv[1:])
