import unittest

from textool import WordStream

class TestWordStream(unittest.TestCase):

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
    suite.addTest(TestWordStream('test_normal_line'))
    suite.addTest(TestWordStream('test_punctuation'))
    suite.addTest(TestWordStream('test_standalone_punctuations'))
    suite.addTest(TestWordStream('test_quotes_and_symbols'))
    suite.addTest(TestWordStream('test_numbers_and_symbols'))
    suite.addTest(TestWordStream('test_only_punctuations'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
