class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        last = 0
        for n in arr:
            delta = n - last
            if delta == 1:
                last = n
                continue
            delta -= 1
            if delta >= k:
                return last + k
            last = n
            k -= delta
        return last + k