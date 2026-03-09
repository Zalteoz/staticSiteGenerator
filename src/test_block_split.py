import unittest
from block_split import *

class BlockSplitTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # 3. Test a single block of text
    def test_single_block(self):
        md = "Just one single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one single block of text."])

    # 4. Test multiple empty blocks (should return empty list)
    def test_empty_input(self):
        md = "\n\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # 5. Test leading and trailing whitespace/newlines
    def test_edge_whitespace(self):
        md = "   \n\nBlock 1\n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1"])


"""
Tests for block type attribution
"""
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###   heading"), BlockType.HEADING)
        
        # Invalid headings
        self.assertEqual(block_to_block_type("####### heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#heading"), BlockType.PARAGRAPH)
        
        # Code
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        
        # Quote
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        
        # Lists
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNDORDERED_LIST)
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. first\n3. second"), BlockType.PARAGRAPH) # Invalid increment

if __name__ == "__main__":
    unittest.main()