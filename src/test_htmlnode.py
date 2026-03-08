import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



"""
Tests for the HTMLNodes
"""
class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Testing if a dictionary of props is correctly converted to a string
        node = HTMLNode(
            tag="a", 
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.google.com" target="_blank"'
        )

    def test_values(self):
        # Testing if the constructor correctly assigns values
        node = HTMLNode(
            tag="p",
            value="This is a paragraph",
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        # Testing that the string representation looks correct
        node = HTMLNode(tag="h1", value="Hello World")
        self.assertEqual(
            repr(node), 
            "HTMLNode('h1', Hello World, children: None, props: None)"
        )

    def test_empty_props(self):
        # Ensuring that None or empty dict returns an empty string
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")


"""
Tests for the leaf nodes
"""
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        # Testing a tag with properties
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_tag(self):
        # Testing raw text rendering
        node = LeafNode(None, "Just some plain text")
        self.assertEqual(node.to_html(), "Just some plain text")

    def test_to_html_no_value(self):
        # Testing the ValueError requirement
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(repr(node), "LeafNode('b', 'Bold text', None)")


"""
Tests for ParentNodes
"""
class TestParentNode(unittest.TestCase):
    # 1. The Basic Case: One level of nesting
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # 2. Deep Nesting: Grandchildren (Testing Recursion)
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # 3. Multiple Children: Mixing tags and raw text
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    # 4. Parent with Properties
    def test_to_html_with_props(self):
        node = ParentNode(
            "a",
            [LeafNode("b", "Bold link")],
            {"href": "https://boot.dev", "class": "primary-btn"}
        )
        # Note: Ensure your props_to_html() handles the space correctly
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" class="primary-btn"><b>Bold link</b></a>'
        )

    # 5. Nested Parent Nodes with their own Props
    def test_nested_parents_with_props(self):
        inner = ParentNode("span", [LeafNode("i", "inner")], {"id": "inner-id"})
        outer = ParentNode("div", [inner], {"class": "container"})
        self.assertEqual(
            outer.to_html(),
            '<div class="container"><span id="inner-id"><i>inner</i></span></div>'
        )

    # 6. Error Handling: Missing Tag
    def test_to_html_error_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "child")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "All parent nodes must have a tag")

    # 7. Error Handling: Missing Children
    def test_to_html_error_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "All parent nodes must have children")

    # 8. Edge Case: Empty Children List
    def test_to_html_empty_children_list(self):
        # A parent with an empty list should still render empty tags
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()