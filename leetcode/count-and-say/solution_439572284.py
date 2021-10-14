def chunk(s):
    last = None
    count = 1
    for c in s:
        if c == last:
            count += 1
        else:
            if last is not None:
                yield last, count
            count = 1
        last = c
    yield last, count

class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return '1'
        out = []
        for c, count in chunk(self.countAndSay(n - 1)):
            out.append(str(count))
            out.append(c)
        return ''.join(out)
        