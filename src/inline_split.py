from textnode import TextType, TextNode
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        #if it's not a text node we just pass through
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: matching delimiter {delimiter!r} not found")

        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.PLAIN))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
            
        new_nodes.extend(split_nodes)
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            parts = original_text.split(f"![{image[0]}]({image[1]})", 1)
            
            if len(parts) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.PLAIN))
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = parts[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
            
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes