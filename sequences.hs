module Sequences (fibonacci, primes, triangle) where

    fibonacci = 1 : 1 : zipWith (+) (fibonacci) (tail fibonacci)

    sieve (x:xs) = 
        let potentialFactors x = [3..(quot x 3)] :: [Integer]
            divides a b = (b `mod` a == 0)
        in x:(filter (\x -> not (any (\b -> b `divides` x) (potentialFactors x))) xs)
    primes :: [Integer]
    primes = 2 : sieve [3,5..]

    triangle = 1 : map (\(i, p) -> i + p) (zip [2..] triangle)