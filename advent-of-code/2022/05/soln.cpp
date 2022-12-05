#include <iostream>

#include "util.hpp"
#include "input.hpp"

using result = apply_moves<
    initial_stacks,
    moves_list
>::value;

template <typename css>
struct get_top_items;

template <typename x, typename xs>
struct get_top_items<cons<x, xs>> {
    using value = cons<typename x::car, typename get_top_items<xs>::value>;
};

template <>
struct get_top_items<nil> {
    using value = nil;
};

template <typename xs>
struct print_charlist;

template <char c, typename xs>
struct print_charlist<cons<charbox<c>, xs>> {
    static inline void run() {
        std::cout << c;
        print_charlist<xs>::run();
    };
};

template <>
struct print_charlist<nil> {
    static inline void run() { };
};

int main() {
    std::cout << "Part 1: ";
    print_charlist<typename get_top_items<result>::value>::run();
    std::cout << std::endl;

    // std::cout << "Part 2: ";
    return 0;
}

