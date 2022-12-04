(require 
  '[clojure.string :as str]
  '[clojure.set :as set])

(def rucksacks
  (str/split-lines (slurp "input")))

(defn split-rucksack [rucksack]
  (def flen (count rucksack))
  (def hlen (/ flen 2))

  (list (set (subs rucksack 0 hlen))
        (set (subs rucksack hlen flen))))

(defn find-same-item [& args]
  (def common (apply set/intersection args))
  (get (into [] common) 0))

(defn get-priority [item]
  (def asciival (int item))
  (cond
    (<= (int \a) asciival (int \z)) (+ 1 (- asciival (int \a)))
    :else (+ 27 (- asciival (int \A)))))

(println
  "Part 1:"
  (apply +
         (map (fn [rsack]
                (let [[l r] (split-rucksack rsack)]
                  (get-priority (find-same-item l r))))
              rucksacks)))

(def groups
  (partition 3 rucksacks))

(println
  "Part 2:"
  (apply +
         (map (fn [g]
                (get-priority (apply find-same-item (map set g))))
              groups)))

