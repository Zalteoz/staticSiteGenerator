import unittest
from gencontent import *

class TestExtractTitle(unittest.TestCase):
    def test_standard_h1(self):
        # Basic check
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_multiline_h1(self):
        # Ensure it finds the H1 among other lines
        md = "Some text\n# Title\nMore text"
        self.assertEqual(extract_title(md), "Title")

    def test_trailing_whitespace(self):
        # Checking that the title is stripped of extra spaces
        self.assertEqual(extract_title("# Hello   "), "Hello")

    def test_no_h1_raises(self):
        # Sad Path: Checks that it actually raises an Exception
        with self.assertRaises(Exception) as cm:
            extract_title("## This is an H2")
        self.assertEqual(str(cm.exception), "Title not found")

    def test_h1_with_no_space(self):
        # Markdown usually requires a space: '#Title' isn't always an H1
        # Your code checks for startswith("# "), so this should raise
        with self.assertRaises(Exception):
            extract_title("#TitleNoSpace")

    def test_multiple_hashes_internal(self):
        # Ensure only the leading hashes are removed
        self.assertEqual(extract_title("# Title with a # inside"), "Title with a # inside")

if __name__ == "__main__":
    unittest.main()