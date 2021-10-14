class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        last = 0
        prev = 0
        for n in nums:
            robThis = max(prev + n, last)
            prev = last
            last = robThis
        return max(last, prev)