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

/// Move crates.
template <int n, int from, int to, typename css>
struct move
    :
    move<
        n - 1,
        from,
        to,
        set_item<
            from,
            cdr<get_item<from, css>>, // tail of [from]
            set_item<
                to,
                cons<
                    car<get_item<from, css>>, // head of [from]
                    get_item<to, css> // [to]
                >,
                css
            >
        >
    > { };

template <int from, int to, typename css>
struct move<0, from, to, css>
    : css { };

int main() {
    return 0;
}
