{-
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a2 + b2 = c2
For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
-}

possibleTriplets = [(a, b, c) | c <- [333..1000], a <- [1..(500 - c `quot` 2)], let b = 1000 - a - c]
isPythagoreanTriplet (a,b,c) = a*a + b*b == c*c

result = a * b * c where (a, b, c) = head (filter isPythagoreanTriplet possibleTriplets)
main = print result  -- 31875000