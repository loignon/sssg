import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            value="site de Ploum",
            props={
                "href": "https://ploum.net",
                "target": "_blank"
            }
        )
        self.assertEqual(node.props_to_html(),' href="https://ploum.net" target="_blank"')

    def test_props_to_html_noprops(self):
        node = HTMLNode(
            value="site de Ploum",
        )
        self.assertEqual(node.props_to_html(),'')
        
    def test_print(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://ploum.net",
                "target": "_blank"
            }
        )
        expected_str = "HTMLNode(a, None, None, {'href': 'https://ploum.net', 'target': '_blank'})"
        self.assertEqual(repr(node), expected_str)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
