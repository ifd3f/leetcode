gridCount :: Int -> Int -> Int -> Int
gridCount side x y = array (0, 100)
    | (x == side || y == side) = 1
    | (x == y) = 2 * right
    | otherwise = right + down
    where right = gridCount side (x + 1) y
          down = gridCount side x (y + 1)

main = print(gridCount 20 1 1)