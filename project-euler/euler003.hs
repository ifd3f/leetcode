{-The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?-}

import Sequences (primes)


largestPrimeFactor n (p:ps)
    | (n == p)         = n  -- n is a prime number
    | (n `mod` p == 0) = largestPrimeFactor (quot n p) (p:ps)  -- p divides n, so we will keep dividing n by p
    | otherwise        = largestPrimeFactor n ps  -- p doesn't divide n, so we will skip p

result = largestPrimeFactor 600851475143 primes

main = print result