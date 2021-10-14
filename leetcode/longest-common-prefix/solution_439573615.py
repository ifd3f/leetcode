class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        chars = []
        if len(strs) == 0:
            return ''
        for i in range(min(len(s) for s in strs)):
            c = strs[0][i]
            for s in strs:
                if s[i] != c:
                    break
            else:
                chars.append(c)
                continue
            break
        return ''.join(chars)