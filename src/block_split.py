from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNDORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()

        if stripped != "":
            filtered_blocks.append(stripped)

    return filtered_blocks

def block_to_block_type(block: str):
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(block) > count and block[count] == " ":
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNDORDERED_LIST
    
    if block.startswith("1. "):
        is_ordered = True
        for i, line in enumerate(lines):
            expected = f"{i + 1}. "
            if not line.startswith(expected):
                is_ordered = False
                break
        
        if is_ordered:
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

