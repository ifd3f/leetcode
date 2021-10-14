def cmpStr(start, a, b):
    for i, c in enumerate(b):
        if a[i + start] != c:
            return False
    return True

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle == '':
            return 0
        if len(needle) > len(haystack):
            return -1
        for i in range(0, len(haystack) - len(needle) + 1):
            if cmpStr(i, haystack, needle):
                return i
        return -1