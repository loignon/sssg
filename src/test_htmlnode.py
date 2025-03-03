import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_notag(self):
        parent_node = ParentNode(tag=None,children=[LeafNode("span", "child")])
        with self.assertRaises(Exception) as ctx:
            parent_node.to_html()

    def test_to_html_nochildren(self):
        parent_node = ParentNode("div",children=None)
        with self.assertRaises(Exception) as ctx:
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
