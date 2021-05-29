"""
Consider a permutation group G that acts on tuples of size n, with each element in the tuple having one of s possible
values. It is possible to calculate the number of orbits of G as follows:
  1. Take the cycle index Z(G), which will be a polynomial of variables a_1, a_2, ..., a_n.
  2. Substitute s into every a_i term.

Now consider two permutation groups G1 and G2 acting on w- and h-tuples respectively. We will define the cartesian
product of G1 and G2 as a new group H acting on w-by-h grids. It is essentially every combination of G1's
permutations acting on the grid's columns, matched with every combination of G2's permutations acting on the grid's
rows.

To find the cycle index of H so that we can count its orbits, we will use a custom mathematical operator on pairs of
cycle index polynomials that I will call the "Cycle Index of Cartesian Product," or CICP for short, which I will write
for convenience as &. For any permutation groups G1 and G2, let H be their cartesian product. The CICP of Z(G1) and
Z(G2) is defined as

    Z(G1) & Z(G2) = Z(H)

The properties of the CICP will be listed in the comments of this program and briefly proven where relevant.
"""
from collections import Counter, defaultdict
from fractions import gcd, Fraction


def prod(iterable):
    """
    Like sum, but it multiplies.
    :param iterable: an iterable
    :return: the product of the items
    """
    p = 1
    for x in iterable:
        p *= x
    return p


class Mono(object):
    """
    Represents a monomial in the cycle index of some group. This monomial does not include any coefficients,
    only a_i factors and their powers. Note that a monomial can be thought of as representing a "species" of
    permutation in some group, where different "species" of permutations have different numbers of cycles of a
    certain length. (1 3 2)(5 4) and (1 4)(3 2 5) would be the same species by this understanding, for example.
    """

    def __init__(self, factors):
        """
        Constructs a monomial.
        :param factors: a dict-like mapping from CI subscripts to its power. For example,
        {3: 8} represents a_3^8.
        """
        self.factors = factors
        self.hash = None

    def __repr__(self):
        return 'Mono(' + repr(dict(self.factors)) + ')'

    def __str__(self):
        return ' '.join('a_{%s}^{%s}' % (s, p) for s, p in self.factors.items())

    def __eq__(self, other):
        return self.factors == other.factors

    def __hash__(self):
        if self.hash is None:
            self.hash = 0
            factors = list(self.factors)
            factors.sort()
            for b in factors:
                p = self.factors[b]
                self.hash <<= 3
                self.hash %= 2 ** 31
                self.hash += b * p
        return self.hash

    def is_one(self):
        """
        There are multiple ways this value can be equivalent to the 1 monomial. For example,
        {3: 0} and {0: 8} are both equivalent to 1.
        :return: if this value is equivalent to 1.
        """
        return all((p == 0 for _, p in self.factors.items()))

    def __mul__(self, other):
        """
        Multiplies two monomials together.
        :param other: a monomial
        :return: their product
        """
        if other.is_one():
            return self
        if self.is_one():
            return other
        return Mono(Counter(self.factors) + Counter(other.factors))

    def __and__(self, other):
        """
        Performs a CICP (see note at top).

        Consider two single-cycle permutations, p1 and p2, of lengths i and j respectively, and p3 being the
        cartesian product of p1 and p2, acting on an i-by-j grid. Z({p1}) = a_i and Z({p2}) = a_j by the definition
        of cycle index.

        By definition of the CICP, Z({p1}) & Z({p1}) = Z({p3}). If you were to count the cycles of p3, you would
        find that it has gcd(i, j) cycles of length lcm(i, j). Therefore by definition of cycle index, a_i & a_j =
        a_{lcm(i, j)}^{gcd(i, j)}.

        Distributive property:
        Now consider a_i & (a_j a_k). This is the cartesian product of a single cycle with two different cycles.
        The cartesian product would apply to a_j and a_k individually, then multiply together to form a single
        large permutation of the grid. Thus, (a_i) & (a_j a_k) = (a_i & a_j) (a_i & a_k). Therefore,
        & distributes across multiplication.

        Associative with exponentiation:
        Since CICP distributes across multiplication, it is also associative with exponentiation
        (i.e. for any b, p, and c: (b ^ p) & c = (c & b) ^ p).

        Zero Property:
        Note that S_0, the 0-degree symmetric group, has cycle index Z(S_0) = 1. This is equivalent to the empty group.
        The cartesian product of any group with the empty group is the empty group, so 1 acts like a zero value for
        CICP (i.e. for any x: x & 1 = 1).

        :param other: the monomial to perform this with.
        :return: the CICP of self and other
        """

        # The zero property of CICP says that if either factor is 1, the result is 1.
        if other.is_one() or self.is_one():
            return CIM_ONE
        result = Counter()

        # CICP distributes across multiplication.
        for f1, p1 in self.factors.items():
            for f2, p2 in other.factors.items():
                # Compute a_i & a_j = a_{lcm(i, j)}^{gcd(i, j)}.

                g = gcd(f1, f2)
                a_pow = g * p1 * p2  # CICP is associative with exponentiation.
                a_sub = (f1 * f2) / g  # LCM in terms of of GCD.
                result[a_sub] += a_pow  # Multiply the resulting monomial by this factor.

        return Mono(result)

    def substitute(self, s):
        """
        Substitutes the value s into every a_1, a_2, ..., a_n.
        :param s: the value to substitute
        :return: the result of the substitution.
        """
        return prod((
            s ** p
            for a, p in self.factors.items()
        ))


class Poly(object):
    """
    Represents a cycle index polynomial.
    """

    def __init__(self, monomials):
        """
        Constructs a monomial.
        :param factors: a dict-like mapping from monomial terms to their coefficients. For example,
        {Mono({3: 8}): Fraction(2, 9)} represents 2/9 * a_3^8.
        """
        self.monomials = monomials

    def __repr__(self):
        return 'Poly(' + repr(dict(self.monomials)) + ')'

    def __eq__(self, other):
        return self.monomials == other.monomials

    def __str__(self):
        return ' + '.join('%s %s' % (c, m) for m, c in self.monomials.items())

    def __mul__(self, other):
        """
        Multiplies this polynomial with another polynomial.
        :param other: another polynomial
        :return: their product
        """
        result = defaultdict(lambda: Fraction(0))
        for m1, c1 in self.monomials.items():
            for m2, c2 in other.monomials.items():
                monomial = m1 * m2
                coeff = c1 * c2
                result[monomial] += coeff
        return Poly(result)

    def __add__(self, other):
        """
        Adds this polynomial to another polynomial, combining like terms.
        :param other: another polynomial
        :return: their sum
        """
        result = defaultdict(lambda: Fraction(0))
        for m, c in self.monomials.items():
            result[m] += c
        for m, c in other.monomials.items():
            result[m] += c
        return Poly(result)

    def scale(self, scalar):
        """
        Multiplies this polynomial by some scalar.
        :param scalar: the scalar
        :return: the product
        """
        return Poly({
            m1: c1 * scalar for m1, c1 in self.monomials.items()
        })

    def __and__(self, other):
        """
        Performs a CICP (see note at top).

        Distributive across addition:
        Consider the product d & (b + c) where d, b, and c are monomials. Since b and c each represent their own
        permutation, we can think of the addition as delineating two different permutations. So, we can define this
        product as presenting the cartesian product of d and b as well as the cartesian product of d and c together.
        In other words, d & (b + c) = (d & b) + (d & c). Therefore, & is distributive across addition.

        :param other: another polynomial
        :return: the CICP of self and other
        """
        result = defaultdict(lambda: Fraction(0))

        # The CPP distributes across addition.
        for m1, c1 in self.monomials.items():
            for m2, c2 in other.monomials.items():
                monomial = m1 & m2  # Perform CICP on the monomial.
                coeff = c1 * c2  # Scalar coefficients are multiplied together.
                result[monomial] += coeff
        return Poly(result)

    def substitute(self, s):
        """
        Substitutes the value s into every a_1, a_2, ..., a_n.
        :param s: the value to substitute
        :return: the result of the substitution.
        """
        return sum((
            c * m.substitute(s)
            for m, c in self.monomials.items()
        ))


CIM_ONE = Mono({})
CIP_ZERO = Poly({})


def symmetric_group_cycle_indices(n):
    """
    Calculates the cycle indices of all symmetric groups up to and including n.

    This is a dynamic programming-based implementation of the recurrence at the end of
    https://en.wikipedia.org/wiki/Cycle_index#Symmetric_group_Sn

    :param n: the maximum symmetric group cycle index to calculate.
    :return: a list of length n + 1 where the cycle index of S_i is at index i of the list.
    """

    sgs = [CIP_ZERO] * (n + 1)  # Initialize all as zero
    sgs[0] = Poly({CIM_ONE: 1})  # Base case: Z(S_0) = 1

    for m in range(1, n + 1):
        for i in range(1, m + 1):
            a_i = Poly({Mono({i: 1}): 1})  # single term a_i
            zs = sgs[m - i]
            sgs[m] += a_i * zs
        sgs[m] = sgs[m].scale(Fraction(1, m))

    return sgs


def solution(w, h, s):
    sgs = symmetric_group_cycle_indices(max(w, h))
    ci = sgs[w] & sgs[h]
    return str(ci.substitute(s))
