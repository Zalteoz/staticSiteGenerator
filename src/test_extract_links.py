import unittest
from extract_links import *

class ExtractLinksTest(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](youtube.com)"
        )
        self.assertListEqual([("link", "youtube.com")], matches)



if __name__ == "__main__":
    unittest.main()
    



