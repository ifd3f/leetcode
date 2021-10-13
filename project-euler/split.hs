nextword :: (Eq a) => a -> [a] -> ([a], [a])
nextword dl (c:cs)
    | cs == [] = ([c], [])
    | (dl == c) = ([], cs)
    | otherwise = ((c:word), remaining)
    where (word, remaining) = nextword dl cs

split :: (Eq a) => a -> [a] -> [[a]]
split dl [] = []
split dl ws = let (word, tailwords) = nextword dl ws in word:(split dl tailwords)

main = do
    print(split ' ' "SAdfasdfs dfsgsfsfg Hghdfh jks j j jsdjfjdj ds kf kdfkj ld")
