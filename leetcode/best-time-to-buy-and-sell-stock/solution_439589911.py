class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 0:
            return 0
        runningMin = prices[0]
        maxProfit = 0
        for n in prices:
            runningMin = min(n, runningMin)
            maxProfit = max(maxProfit, n - runningMin)
        return maxProfit