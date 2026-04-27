from enum import Enum


BlockType = Enum('BlockType', [
    'paragraph',
    'heading',
    'code',
    'quote',
    'unordered_list',
    'ordered_list'
])

def markdown_to_blocks(markdown):
    return [s.strip() for s in markdown.split('\n\n') if s]

def block_to_block_type(block):
    heading_level = 0
    for c in block:
        if c == '#':
            heading_level += 1
        else:
            break
    if heading_level > 0:
        return BlockType.heading

    lines = block.split('\n')

    if len(lines) > 1 and lines[0] == '```' and lines[-1] == '```': #code
        return BlockType.code

    isQuote = True
    isUL = True
    for line in lines:
        if line[0] != '>': isQuote = False
        if len(line) > 2 and not line.startswith('- '): isUL = False
    if isQuote:
        return BlockType.quote
    if isUL:
        return BlockType.unordered_list

    isOL = True
    if not (len(lines) > 2 and lines[0][:2] == '1. '):
        isOL = False
    else:
        current_num = 1
        for line in lines:
            first_word = line.split(' ',2)[0]
            if len(first_word) > 1 and first_word[-1] == '.':
                next_number = int(first_word[:-1])
                if next_number != current_num+1:
                    isOL = False
                    break
    if isOL:
        return BlockType.ordered_list
    return BlockType.paragraph
