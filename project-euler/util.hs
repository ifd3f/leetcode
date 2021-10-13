module Util (window, transpose, primeFactors, factorCount) where
    import Sequences (primes)

    window :: Int -> [a] -> [[a]]
    window _ [] = []
    window s xs = if length section < s then [] else (section) : (window s (tail xs))
        where section = take s xs

    fullJoin :: Ord a => [a] -> [a] -> [a]
    fullJoin [] bs = bs
    fullJoin as [] = as
    fullJoin (a:as) (b:bs)
        | (a == b) = a : (fullJoin as bs)
        | (a < b) = a : (fullJoin as (b:bs))
        | (a > b) = b : (fullJoin (a:as) bs)

    transpose :: [[a]] -> [[a]]
    transpose mat = if hasEmpty then [] else (firstCol : transpose rest)
        where
            hasEmpty = any null mat
            firstCol = map head mat
            rest = map tail mat

    primeFactors :: Integer -> [Integer]
    primesImpl n (p:ps)
        | (n == 1) = []
        | (n `mod` p == 0) = p : (primesImpl (n `quot` p) (p:ps))
        | otherwise = primesImpl n ps
    primeFactors n = primesImpl n primes
    
    countFirst :: [Integer] -> Int
    countFirst (x:xs) = 1 + length (takeWhile (==x) xs)
    
    factorCount :: Integer -> Integer
    factorCount n = toInteger (product (map (+1) (group factors)))
        where 
            factors = primeFactors n
            group [] = []
            group fs = count : group (drop count fs)
                where count = countFirst fs
