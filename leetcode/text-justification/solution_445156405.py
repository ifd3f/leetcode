def spread(words, width, lj):
    if len(words) == 1 or lj:
        out = ' '.join(words)
        return out + (width - len(out)) * ' '
    
    spaceCount = len(words) - 1
    spaces = width - sum(len(x) for x in words)
    minWidth = spaces // spaceCount
    expandCount = spaces % spaceCount
    
    print(spaceCount, spaces, minWidth, expandCount)
    
    out = [words[0]]
    for i in range(1, len(words), 1):
        out.append(' ' * minWidth)
        if i <= expandCount:
            out.append(' ')
        out.append(words[i])
    return ''.join(out)
    

def chunkWords(words, maxWidth):
    words.reverse()
    thisGroup = []
    groups = [thisGroup]
    leftInGroup = maxWidth
    while len(words) > 0:
        w = words.pop()
        subtractAmount = len(w)
        if len(thisGroup) > 0:
            subtractAmount += 1
        if leftInGroup >= subtractAmount:
            leftInGroup -= subtractAmount
            thisGroup.append(w)
        else:
            thisGroup = [w]
            groups.append(thisGroup)
            leftInGroup = maxWidth - len(w)
    return groups

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        lines = chunkWords(words, maxWidth)
        print(lines)
        return [spread(line, maxWidth, i == len(lines) - 1) for i, line in enumerate(lines)]