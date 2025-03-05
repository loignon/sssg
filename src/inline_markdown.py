import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        splits = node.text.split(delimiter)
        if len(splits)%2 == 0:
            raise ValueError(f"one '{delimiter}' does not close")
        for i, text in enumerate(splits):
            if not text: continue
            if i%2:
                new_nodes.append(TextNode(text, text_type))
            elif i%2==0:
                new_nodes.append(TextNode(text, node.text_type))
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in images:
            splits = remaining_text.split(f"![{alt_text}]({url})",1)
            if len(splits) != 2:
                raise ValueError("malformed markdown, an image did not close")
            if splits[0]:
                new_nodes.append(TextNode(splits[0], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = splits[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, node.text_type))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in links:
            splits = remaining_text.split(f"[{alt_text}]({url})",1)
            if len(splits) != 2:
                raise ValueError("malformed markdown, a link did not close")
            if splits[0]:
                new_nodes.append(TextNode(splits[0], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            remaining_text = splits[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, node.text_type))
    return new_nodes

def extract_markdown_images(text):
    expr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(expr, text)

def extract_markdown_links(text):
    expr = r"(?<!!)\[(.*)\]\((.*)\)"
    return re.findall(expr, text)
