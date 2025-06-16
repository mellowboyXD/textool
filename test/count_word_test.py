import unittest

from textool import count_words

class WordCountTest(unittest.TestCase):
    def test_normal(self):
        ws = ["Hello", "world", "hello", "WORLD"]
        expected = {"hello": 2, "world": 2}
        output = count_words(ws)
        self.assertDictEqual(output, expected, "Normal test")

    def test_case_sensitive(self):
        ws = ["Hello", "world", "hello", "WORLD"]
        expected = {"Hello": 1, "world": 1, "hello": 1, "WORLD": 1}
        output = count_words(ws, case_sensitive=True)
        self.assertDictEqual(output, expected, "Test case sensitivity")

    def test_non_alpha(self):
        ws = ["hello", "world", "123", "hello!", "good"]
        expected = {"hello": 1, "world": 1, "good": 1}
        output = count_words(ws, lambda x: x.isalpha())
        self.assertDictEqual(output, expected, "Test non alpha streams")

    def test_filter_min_length(self):
        ws = ["hi", "hello", "hi", "yes", "wow", "no"]
        expected = {"hello": 1, "yes": 1, "wow": 1}
        output = count_words(ws, lambda x: x.isalpha(), min_length=3)
        self.assertDictEqual(output, expected, "Test min_length")

    def test_max_item(self):
        ws = ["a", "b", "a", "c", "b", "a", "d"]
        expected = {"a": 3, "b": 2}
        output = count_words(ws, max_items=2)
        self.assertDictEqual(output, expected, "Test max_length")

    def test_all(self):
        ws = ["Test", "TEST", "123", "pass", "PASS", "!!!", "Pass"]
        expected = {"Test": 1, "TEST": 1, "pass": 1, "PASS": 1, "Pass": 1}
        output = count_words(ws,
                             lambda x: x.isalpha(),
                             case_sensitive=True,
                             min_length=4)
        self.assertDictEqual(output, expected, "Test all")


def suite():
    suite = unittest.TestSuite()
    test_cases = [func for func in dir(WordCountTest)
        if callable(getattr(WordCountTest, func)) and func.startswith("test")]
    for test_case in test_cases:
        suite.addTest(WordCountTest(test_case))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
