#pragma once

/// Represents an empty list.
struct nil { };

template <typename _car, typename _cdr>
struct cons {
    using car = _car;
    using cdr = _cdr;
};

/// Helper to construct a list.
template <typename... xs>
struct list;

template <>
struct list<> { 
    using value = nil;
};

template <typename x, typename... xs>
struct list<x, xs...> {
    using value = cons<x, typename list<xs...>::value>;
};

template <char x>
struct charbox {
    static char value() {
        return x;
    }
};

/// Gets the i-th type of the given list.
template <int i, typename xs>
struct get_item;

template <int i, typename x, typename xs>
struct get_item<i, cons<x, xs>> {
    using value = typename get_item<i - 1, xs>::value;
};

template <typename x, typename xs>
struct get_item<0, cons<x, xs>> {
    using value = x;
};

template <int i>
struct get_item<i, nil>;  // out of bounds

/// Sets the i-th type of the given list to x.
template <int i, typename x, typename xs>
struct set_item;

template <typename x, typename h, typename t>
struct set_item<0, x, cons<h, t>> {
    using value = cons<x, t>;
};

template <int i, typename x, typename h, typename t>
struct set_item<i, x, cons<h, t>> {
    using value = cons<h, typename set_item<i - 1, x, t>::value>;
};

template <int i, typename x>
struct set_item<i, x, nil>; // out of bounds

/// Takes the top N items from the list
template <int n, typename xs>
struct take;

template <typename x, typename xs>
struct take<0, cons<x, xs>> {
    using value = nil;
};

template <>
struct take<0, nil> {
    using value = nil;
};

template <int n, typename x, typename xs>
struct take<n, cons<x, xs>> {
    using value = cons<x, typename take<n - 1, xs>::value>;
};

template <int n>
struct take<n, nil>;

/// Drops the top N items from the list
template <int n, typename xs>
struct drop;

template <typename x, typename xs>
struct drop<0, cons<x, xs>> {
    using value = cons<x, xs>;
};

template <>
struct drop<0, nil> {
    using value = nil;
};

template <int n, typename x, typename xs>
struct drop<n, cons<x, xs>> {
    using value = typename drop<n - 1, xs>::value;
};

template <int n>
struct drop<n, nil>;

/// Appends the two lists together
template <typename xs, typename ys>
struct concat;

template <typename x, typename xs, typename ys>
struct concat<cons<x, xs>, ys> {
    using value = cons<x, typename concat<xs, ys>::value>;
};

template <typename ys>
struct concat<nil, ys> {
    using value = ys;
};

/// Representation of a move.
template <int n, int from, int to>
struct move {
    /// Apply this move to a crate stack set.
    template <typename css>
    struct apply {
        using value = typename move<n - 1, from, to>::apply<
            typename set_item<
                from - 1,
                typename get_item<from - 1, css>::value::cdr, // tail of [from]
                typename set_item<
                    to - 1,
                    cons<
                        typename get_item<from - 1, css>::value::car, // head of [from]
                        typename get_item<to - 1, css>::value // [to]
                    >,
                    css
                >::value
            >::value
        >::value;
    };

    template <typename css>
    struct apply2 {
        using value = typename set_item<
            from - 1,
            typename drop<
                n,
                typename get_item<from - 1, css>::value
            >::value, // tail of [from]
            typename set_item<
                to - 1,
                typename concat<
                    typename take<
                        n,
                        typename get_item<from - 1, css>::value
                    >::value, // head of [from]
                    typename get_item<to - 1, css>::value // [to]
                >::value,
                css
            >::value
        >::value;
    };
};

template <int from, int to>
struct move<0, from, to> {
    template <typename css>
    struct apply {
        using value = css;
    };

    template <typename css>
    struct apply2 {
        using value = css;
    };
};

template <typename css, typename moves_list>
struct apply_moves;

template <typename css, typename h, typename rest>
struct apply_moves<css, cons<h, rest>> {
    using value = typename apply_moves<
        typename h::apply<css>::value,
        rest
    >::value;
};

template <typename css>
struct apply_moves<css, nil> {
    using value = css;
};

template <typename css, typename moves_list>
struct apply_moves2;

template <typename css, typename h, typename rest>
struct apply_moves2<css, cons<h, rest>> {
    using value = typename apply_moves2<
        typename h::apply2<css>::value,
        rest
    >::value;
};

template <typename css>
struct apply_moves2<css, nil> {
    using value = css;
};

