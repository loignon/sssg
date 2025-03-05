import unittest
from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import TextNode, TextType


class TestSplittingNodes(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_empty_delimiter_at_start(self):
        node = TextNode("``not code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("not code block", TextType.TEXT),
        ])

    def test_no_split(self):
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block", TextType.CODE),
        ])

    def test_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_malformed_markdown(self):
        node = TextNode("Some malformed **markdown", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

class TestLinkExtraction(unittest.TestCase):
    def test_image(self):
        text = "This is text with an ![image](https://blabla.meh/some.png)"
        self.assertEqual(extract_markdown_images(text),
            [('image', 'https://blabla.meh/some.png')]
        )

    def test_link(self):
        text = "This is text with a [regular link](https://blabla.meh)"
        self.assertEqual(extract_markdown_links(text),
            [('regular link', 'https://blabla.meh')]
        )

    def test_link_on_image(self):
        text = "This is text with an ![image](https://blabla.meh/some.png)"
        self.assertEqual(extract_markdown_links(text), [])

class TestSplittingNodesImages(unittest.TestCase):
    def test_single_image_at_end(self):
        text = "This is text with an ![image](https://blabla.meh/some.png)"
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_images([node]),[
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://blabla.meh/some.png")
        ])

    def test_single_image_at_start(self):
        text = "![image](https://blabla.meh/some.png) and some text."
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_images([node]),[
            TextNode("image", TextType.IMAGE, "https://blabla.meh/some.png"),
            TextNode(" and some text.", TextType.TEXT),
        ])

    def test_single_image_in_middle(self):
        text = "This is text with an ![image](https://blabla.meh/some.png) and some text."
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_images([node]),[
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://blabla.meh/some.png"),
            TextNode(" and some text.", TextType.TEXT),
        ])
    def test_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ])

class TestSplittingNodesLinks(unittest.TestCase):
    def test_single_link_at_end(self):
        text = "This is text with a [link](https://blabla.meh/some.png)"
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_links([node]),[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://blabla.meh/some.png")
        ])

    def test_single_link_at_start(self):
        text = "[link](https://blabla.meh/some.png) and some text."
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_links([node]),[
            TextNode("link", TextType.LINK, "https://blabla.meh/some.png"),
            TextNode(" and some text.", TextType.TEXT),
        ])

    def test_single_link_in_middle(self):
        text = "This is text with a [link](https://blabla.meh/some.png) and some text."
        node = TextNode(text, TextType.TEXT)
        self.assertEqual(split_nodes_links([node]),[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://blabla.meh/some.png"),
            TextNode(" and some text.", TextType.TEXT),
        ])

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()
