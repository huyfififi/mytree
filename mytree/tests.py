import unittest

from mytree.main import suffix


class TestSuffix(unittest.TestCase):
    def test_suffix(self):
        result = suffix("file.txt")
        expected_result = "txt"
        self.assertEqual(result, expected_result)

        result = suffix("file.tar.gz")
        expected_result = "gz"
        self.assertEqual(result, expected_result)

        result = suffix("file")
        expected_result = "file"
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
