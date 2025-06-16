from typing import Iterable
import unittest

from test.count_word_test import WordCountTest
from textool import WordStream

class TestWordStream(unittest.TestCase):

    def test_is_iter(self):
        line = "Hello world"
        ws = WordStream(line)
        self.assertTrue(isinstance(ws, Iterable), "Test if iterable")

    def test_normal_line(self):
       line = "Hello this is a line single line";
       expected = line.split()
       ws = WordStream(line)
       for i, expect in enumerate(expected):
           with self.subTest(i=i):
               n = next(ws)
               #print(n)
               self.assertEqual(n, expect)

    def test_punctuation(self):
        line = "The quick,b brown fox jumps over the lazy dog.";
        ws = [x for x in WordStream(line)]
        expected = ["The", "quick", "b", "brown", "fox", "jumps", "over", "the", 
                    "lazy", "dog"]
        self.assertEqual(ws, expected, "Sentence with punctuations")

    def test_standalone_punctuations(self):
        line = "Wait... what?! No way!!!"
        expected = ["Wait", "what", "No", "way"]
        ws = [x for x in WordStream(line)]
        self.assertEqual(ws, expected, "Sentence with standalone punctuations")

    def test_quotes_and_symbols(self):
        line = '"Hello," said the AI. "Let\'s go!"'
        ws = [x for x in WordStream(line)]
        expected = ["Hello", "said", "the", "AI", "Let", "s", "go"]
        self.assertEqual(ws, expected, "Sentences with quotes and symbols")

    def test_numbers_and_symbols(self):
        line = "123 @#$%^ hello 456!"
        expected = ["123", "hello", "456"]
        ws = [x for x in WordStream(line)]
        self.assertEqual(ws, expected, "Sentence with numbers and symbols")

    def test_only_punctuations(self):
        line = "...!?--@@##"
        expected = []
        ws = [x for x in WordStream(line)]
        self.assertEqual(ws, expected, "Sentences with punctuations only")

def suite():
    suite = unittest.TestSuite()
    test_cases = [func for func in dir(TestWordStream)
        if callable(getattr(TestWordStream, func)) and func.startswith("test")]
    for test_case in test_cases:
        suite.addTest(TestWordStream(test_case))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
