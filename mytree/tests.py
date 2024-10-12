import unittest
from unittest.mock import mock_open, patch

from main import get_filenames_to_ignore


class TestConfig(unittest.TestCase):
    def test_get_filenames_to_ignore_file_exists(self):
        # Mock content for the ~/.mytreeignore file
        mock_file_content = (
            "# Ignore comment\nfile1.txt\nfile2.txt\n\n# Another comment\nfile3.txt"
        )

        # Use mock_open to simulate open() and provide mock_file_content
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = get_filenames_to_ignore()

        expected_result = ["file1.txt", "file2.txt", "file3.txt"]
        self.assertEqual(result, expected_result)

    def test_get_filenames_to_ignore_file_not_found(self):
        # Simulate FileNotFoundError when open() is called
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = get_filenames_to_ignore()

        expected_result = []
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
