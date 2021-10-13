multiplesOf3 = [x | x <- [1..1000], x `mod` 3 == 0]
multiplesOf5 = [x | x <- [1..1000], x `mod` 3 == 0]

main = print(sum(multiplesOf3 ++ multiplesOf5)) 