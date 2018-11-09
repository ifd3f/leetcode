{-The sum of the squares of the first ten natural numbers is,

12 + 22 + ... + 102 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)2 = 552 = 3025
Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.-}

sumFirstN n = n * (n + 1) `quot` 2
sumSquaredN n = n * (n + 1) * (2 * n + 1) `quot` 6

result = (sumFirstN 100)^2 - sumSquaredN 100