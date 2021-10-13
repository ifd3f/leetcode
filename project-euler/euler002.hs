--import Debug.Trace (trace)
import Sequences

main = print(sum (filter (\x -> mod x 2 == 0) (takeWhile (<4000000) fibonacci)))