import unittest
from textnode import TextNode, TextType
from inline_split import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodes(unittest.TestCase):

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_multiple(self):
        node = TextNode("This is **bold** and **more bold**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("more bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_at_start(self):
        node = TextNode("`code` at the start", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode(" at the start", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_exception_missing_delimiter(self):
        node = TextNode("This is `invalid code", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)



class TestSplitLinksAndImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Check [Boot.dev](https://www.boot.dev) or [Google](https://www.google.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.PLAIN),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" or ", TextType.PLAIN),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("Just plain text here", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


"""
Test of the complete suite of functions
"""
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_no_formatting(self):
        text = "Just a plain old string with nothing special."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.PLAIN)], nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "**Bold Start** and **Bold End**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Bold Start", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("Bold End", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_mix_bold_italic(self):
        # Testing that ** and _ don't conflict
        text = "This is **bold** and this is _italic_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()