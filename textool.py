#!/bin/python3.13

import sys
import traceback
from datetime import datetime
from enum import Enum
from typing import Callable, Iterable, Iterator

cmd_options = {"-f": "--freq", "-u": "--unique", "-l": "--lengths"}
log_file = None  # Logs to stdout


class StreamHandler:
    def __init__(self, stream: str | None = None):
        if stream is not None:
            self.stream = open(stream, "a")
        else:
            self.stream = sys.stdout

    def write(self, record):
        if self.stream:
            try:
                self.stream.write(record)
                self.stream.flush()
            except Exception as err:
                print(f"Error Writing Log: {err}")

    def close(self):
        try:
            self.stream.flush()
            self.stream.close()
        except Exception as err:
            print(f"Error Closing Log: {err}")


handle = StreamHandler(log_file)


def log_errors(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        time = datetime.now().strftime("%d/%m/%YYYY, %H:%M:%S")
        try:
            return func(*args, **kwargs)
        except UsageError as err:
            print(f"[USAGE]: {err}")
        except Exception as err:
            handle.write(f"[LOG] {time}: {err}\n{traceback.format_exc()}")

    return wrapper


class Options(Enum):
    FREQ = 0
    UNIQ = 1
    LEN = 2


short_options = list(cmd_options.keys())
long_options = list(cmd_options.values())


class UsageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = f"ERROR: {message}"

    def error_and_exit(self):
        print(f"ERROR: {self.message}")
        print(f"Options: {long_options}")
        exit()


class InvalidArgs(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class WordStream:
    w = []

    def __init__(self, line):
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


@log_errors
def read_file(path: str) -> Iterator[str]:
    try:
        with open(path, "r") as file:
            for line in file:
                _ = line.encode("utf-8")
                yield line
    except FileNotFoundError:
        raise UsageError(f"'{path}' does not exist.")
    except IsADirectoryError:
        raise UsageError(f"'{path}' is a directory.")
    except UnicodeDecodeError as err:
        print(f"Could not decode '{path}'.")
        raise IOError(err)


@log_errors
def count_words(
    ws: Iterable[str], *filters, case_sensitive=False, **kwargs
) -> dict[str, int]:
    """
    `ws` - Any iterable of words
    `*filters` - Are callables that filters for specific words
    `case_sensitive` - Toggles normalization
    `**kwargs` - May include `min_length`, `max_items`

        returns a dictionary containing filtered words and their corresponding
        count
    """
    options = kwargs.copy()
    max_items = options.pop("max_items", None)
    min_length = options.pop("min_length", None)
    max_length = options.pop("max_length", None)

    if options:
        raise InvalidArgs(f"Undefined Keyword Arguments {options}")

    counter = {}
    for word in ws:
        word: str = word if case_sensitive else word.lower()

        skip = False
        for filter in filters:
            if not callable(filter):
                raise InvalidArgs("Filters must be callables")

            if not isinstance(filter("mellowboyXD"), bool):
                raise InvalidArgs("Filters take in `str` and returns `bool`")

            if not filter(word):
                skip = True
                break

        if skip:
            continue

        if min_length and len(word) < min_length:
            continue

        if max_length and len(word) > max_length:
            continue

        if word in counter:
            counter[word] += 1
        else:
            if max_items:
                if len(counter) < max_items:
                    counter[word] = 1
            else:
                counter[word] = 1

    return counter


@log_errors
def main(*args) -> None:
    argc = len(args)

    if argc < 1:
        raise UsageError("Not enough arguments")

    # Handle args
    opts = set()
    fileName = ""
    error_invalid_flag = False
    invalid_flags = []
    for c in args:
        if c in short_options:
            opts.add(Options(short_options.index(c)))
        elif c in long_options:
            opts.add(Options(short_options.index(c)))
        elif c[0] != "-":
            fileName = c
        else:
            error_invalid_flag = True
            invalid_flags.append(c)

    # User types a command that is not valid
    if error_invalid_flag:
        raise UsageError(f"Invalid command. {invalid_flags}")

    # User does not provide file name
    if not fileName:
        raise UsageError("File input not provided")

    for line in read_file(fileName):
        stream = WordStream(line)
        count = count_words(stream)
        print(count)


if __name__ == "__main__":
    try:
        main(*sys.argv[1:])
    finally:
        handle.close()
