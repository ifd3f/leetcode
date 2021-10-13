{-
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
-}

rDigitString :: Integer -> [Integer]
rDigitString n
    | (n < 10) = [n]
    | otherwise = (n `mod` 10) : rDigitString (n `quot` 10)

combineIntString :: [Integer] -> Integer
combineIntString (a:xs) = if xs == [] then a
    else combineIntString ((a * 10 + b):ys) where b:ys = xs

powerOfTen :: Integer -> Integer
powerOfTen n
    | (n < 10) = 0
    | otherwise = 1 + powerOfTen (quot n 10)

isPalindrome :: Eq a => [a] -> Bool
isPalindrome xs = (left == right) where
    splitLength = (length xs) `quot` 2
    left = take splitLength xs
    right = take splitLength (reverse xs)

productStrings = [rDigitString (x * y) | x <- [100..999], y <- [100..x]]
palindromes = map (combineIntString . reverse) (filter isPalindrome productStrings)
result = maximum palindromes
