#lang racket

(define in (file->lines "./input"))

(define/match (input->elves xs)
  [('()) '()]
  [((cons "" rest)) (cons '() (input->elves rest))]
  [((cons a rest))
   (define calories (string->number a))
   (match (input->elves rest)
     ['() (list (list calories))]
     [(cons next-elf rest-elves) (cons (cons calories next-elf) rest-elves)])])

(define elves (input->elves in))

elves

(println "Part 1")
(define calorie-totals (map (λ (x) (apply + x)) elves))
(apply max calorie-totals)

(println "Part 2")
(apply + (take (sort calorie-totals >=) 3))