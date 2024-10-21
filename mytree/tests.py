import unittest
from unittest.mock import patch

from mytree.main import suffix, MyTreeConfig


class TestMyTreeConfig(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    def test_default_config(self, mock_exists):
        config = MyTreeConfig()
        self.assertEqual(config.filenames_to_ignore, [".git", "__pycache__"])
        self.assertEqual(config.directory_color, 202)
        self.assertEqual(config.file_colors, {"py": 14})

        mock_exists.assert_called_once()


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
