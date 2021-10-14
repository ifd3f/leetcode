class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        largest = nums[0]
        maxSeqEndingHere = nums[0]
        for i in range(1, len(nums)):
            n = nums[i]
            maxSeqEndingHere = max(maxSeqEndingHere + n, n)
            largest = max(maxSeqEndingHere, largest)
        return largest