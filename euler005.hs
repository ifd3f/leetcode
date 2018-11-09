{-
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
-}

import Sequences (primes)

primeFactors :: Integer -> [Integer]
primesImpl n (p:ps)
    | (n == 1) = []
    | (n `mod` p == 0) = p : (primesImpl (n `quot` p) (p:ps))
    | otherwise = primesImpl n ps
primeFactors n = primesImpl n primes

fullJoin :: Ord a => [a] -> [a] -> [a]
fullJoin [] bs = bs
fullJoin as [] = as
fullJoin (a:as) (b:bs)
    | (a == b) = a : (fullJoin as bs)
    | (a < b) = a : (fullJoin as (b:bs))
    | (a > b) = b : (fullJoin (a:as) bs)

{-mutuallyExclusive (a:as) (b:bs)
    | a == b = False
    | a < b = mutuallyExclusive as (b:bs)
    | a > b = mutuallyExclusive (a:as) bs
    | as == [] || bs == [] = True-}

factorSets = map primeFactors [20,19..1]
combinedFactors = foldl fullJoin [] factorSets
result = product combinedFactors
