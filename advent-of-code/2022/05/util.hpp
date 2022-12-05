#pragma once

/// Represents an empty list.
struct nil { };

template <typename _car, typename _cdr>
struct cons { };

/// Returns the first item of the cons.
template <typename _cons>
struct car;

template <typename _car, typename _cdr>
struct car<cons<_car, _cdr>>
    : _car { };

/// Returns the second item of the cons.
template <typename _cons>
struct cdr;

template <typename _car, typename _cdr>
struct cdr<cons<_car, _cdr>>
    : _cdr { };

/// Helper to construct a list.
template <typename... xs>
struct list
    : nil { };

template <typename x, typename... xs>
struct list<x, xs...>
    : cons<x, list<xs...>> { };

template <char x>
struct charbox {
    static char value() {
        return x;
    }
};

/// Gets the i-th type of the given list.
template <int i, typename xs>
struct get_item;

template <typename x, typename xs>
struct get_item<0, cons<x, xs>>
    : x { };

template <int i, typename x, typename xs>
struct get_item<i, cons<x, xs>>
    : get_item<i - 1, xs> { };

/// Sets the i-th type of the given list to x.
template <int i, typename x, typename xs>
struct set_item;

template <typename x, typename h, typename t>
struct set_item<0, x, cons<h, t>>
    : cons<x, t> { };

template <int i, typename x, typename h, typename t>
struct set_item<i, x, cons<h, t>>
    : set_item<i - 1, x, t> { };

template <int i, typename x>
struct set_item<i, x, nil>
    : nil { };

/// Representation of a move.
template <int n, int from, int to>
struct move {
    /// Apply this move to a crate stack set.
    template <typename css>
    struct apply
        :
        move<n - 1, from, to>::apply<
            set_item<
                from - 1,
                cdr<get_item<from - 1, css>>, // tail of [from]
                set_item<
                    to - 1,
                    cons<
                        car<get_item<from - 1, css>>, // head of [from]
                        get_item<to - 1, css> // [to]
                    >,
                    css
                >
            >
        > { };
};

template <int from, int to>
struct move<0, from, to> {
    template <typename css>
    struct apply
        : css { };
};

template <typename css, typename moves_list>
struct apply_moves;

template <typename css>
struct apply_moves<css, nil>
    : css { };

template <typename css, typename h, typename rest>
struct apply_moves<css, cons<h, rest>>
    : apply_moves<typename h::apply<css>, rest> { };

