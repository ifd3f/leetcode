def spread(words, width, lj):
    if len(words) == 1 or lj:
        out = ' '.join(words)
        return out + (width - len(out)) * ' '
    
    spaceCount = len(words) - 1
    spaces = width - sum(len(x) for x in words)
    minWidth = spaces // spaceCount
    expandCount = spaces % spaceCount
        
    out = [words[0]]
    for i in range(1, len(words), 1):
        out.append(' ' * minWidth)
        out.append(words[i])
    out.append(' ' * expandCount)
    return ''.join(out)

class Solution:
    def reorderSpaces(self, text: str) -> str:
        return spread(text.split(), len(text), False)