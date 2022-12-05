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

int main() {
    std::cout << typeid(result).name();
    return 0;
}

