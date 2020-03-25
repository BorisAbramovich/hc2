from __future__ import absolute_import

import math as _math
import decimal as _decimal
import itertools as _itertools
import collections as _collections

from math import factorial

from basics.itertools import indexify_no_args

try:
    from math import gcd as _gcd
except ImportError:
    from fractions import gcd as _gcd


def math_product(iterable):
    """
    Return the mathematical product of an iterable. Similar to `sum`.

    >>> math_product([1, 2, 3])
    6
    >>> math_product([])
    Traceback (most recent call last):
    ValueError: math_product of an empty set is undefined.
    """
    iterable = iter(iterable)
    try:
        prod = next(iterable)
    except StopIteration:
        raise ValueError('math_product of an empty set is undefined.')
    for i in iterable:
        prod *= i
    return prod


def digits(num):
    """
    Return the decimal digits in an integer.

    >>> digits(12345)
    [1, 2, 3, 4, 5]
    """
    return [int(c) for c in str(num)]


@indexify_no_args()
def fibs():
    """
    Ordered fibonacci numbers.

    >>> list(fibs[:5])
    [1, 2, 3, 5, 8]
    """
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield b


def factors(num):
    """
    Return an ordered list of the prime factors of a number.

    >>> factors(12)
    [2, 2, 3]
    """
    if num < 1:
        raise ValueError('num must be positive')
    elif num == 1:
        return [1]

    factor_list = []
    i = 2
    iter_limit = isqrt(num)
    while i <= iter_limit:
        if num % i == 0:
            while num % i == 0:
                factor_list.append(i)
                num = num // i
            iter_limit = isqrt(num)
        i += 1
    if num != 1:
        factor_list.append(num)
    return factor_list


def gcd(nums):
    """
    Return the greatest common divisor of the given numbers.

    >>> gcd([8, 12, 16, 100])
    4
    """
    iter_nums = iter(nums)
    res = next(iter_nums)
    for i in iter_nums:
        res = _gcd(res, i)
    return res


def lcm(nums):
    """
    Return the least common multiplier of the given numbers.

    >>> lcm([3, 4, 6])
    12
    """
    iter_nums = iter(nums)
    res = next(iter_nums)
    for i in iter_nums:
        if res == 0:
            return 0
        res = res // _gcd(res, i) * i
    return res


def is_prime(num):
    """
    Return whether num is prime.

    >>> is_prime(17), is_prime(4)
    (True, False)
    """
    if num < 0:
        raise ValueError('num must be 0 or greater')
    elif num < 2:
        return False
    else:
        return not any((num % i == 0) for i in range(2, isqrt(num) + 1))


@indexify_no_args()
def primes():
    """
    Ordered list of primes.

    >>> list(primes[:5])
    [2, 3, 5, 7, 11]
    """
    return filter(is_prime, _itertools.count(2))


def divisor_count(num):
    """
    Return the amount of divisors of a number.
    Note that if ``num = p1^a1 * p2^a2 * ...``
    then the amount of divisors for num is ``(a1+1) * (a2+1) * ...``

    >>> divisor_count(11)
    2
    >>> divisor_count(12)
    6
    """
    if num < 2:
        return num
    else:
        return math_product(i + 1 for i in _collections.Counter(factors(num)).values())


def divisors(num):
    """
    Return all divisors of a number.

    Unoptimized: O(num)

    >>> divisors(12)
    [1, 2, 3, 4, 6, 12]
    """
    divisor_list = []
    for i in range(1, num // 2 + 1):
        if num % i == 0:
            divisor_list.append(i)
    divisor_list.append(num)
    return divisor_list


def long_division(n, d):
    """
    Return the exact value of the division of two numbers. Parenthesis mean that the
    numbers inside are repeated indefinitely.

    >>> long_division(13, 7)
    '1.(857142)'
    """
    units, remainder = divmod(n, d)
    if not remainder:
        return str(units)
    remainder *= 10
    fraction = ''
    seen_remainders = []
    while remainder:
        if remainder in seen_remainders:
            loop_start_idx = seen_remainders.index(remainder)
            return '{}.{}({})'.format(units, fraction[:loop_start_idx], fraction[loop_start_idx:])
        seen_remainders.append(remainder)
        q, remainder = divmod(remainder, d)
        fraction += str(q)
        remainder *= 10
    return '{}.{}'.format(units, fraction)


def rotations(num):
    """
    Return all decimal digit rotations of an integer

    >>> rotations(1234)
    [1234, 2341, 3412, 4123]
    """
    rotation_list = []
    curr = str(num)
    for i in range(len(curr)):
        rotation_list.append(curr)
        curr = curr[1:] + curr[:1]
    return [int(i) for i in rotation_list]


def over(n, k):
    """
    Return n over k. The formula is ``n! / (k! * (n-k)!)``

    >>> over(10, 2)
    45
    >>> over(5, 5)
    1
    """
    k = max(k, n - k)
    if k == n:
        return 1
    return math_product(range(k + 1, n + 1)) // factorial(n - k)


def sum_mod(iterable, modulus):
    """
    Return the sum of the numbers in `iterable` modulo `modulus`.
    """
    s = 0
    for i in iterable:
        s = (s + i) % modulus
    return s


def _isqrtd(n):
    """
    See `isqrt`.

    >>> for i in range(400):
    ...     n = 10 ** i
    ...     assert _isqrtd(n) ** 2 <= n < (_isqrtd(n) + 1) ** 2
    """
    dec_n = _decimal.Decimal(n)
    with _decimal.localcontext() as ctx:
        ctx.prec = int(dec_n.log10()) // 2 + 3  # Just some extra precision
        res = int(dec_n.sqrt())
    for i in range(1, -2, -1):
        if (res + i) ** 2 <= n:
            # if i != 0:
            #     print('Weird results for n = %s', n)
            return res + i
    else:
        raise AssertionError


def isqrt(n):
    """
    Similar to ``int(math.sqrt(n))`` but is accurate unlike ``math.sqrt`` which has accuracy problems.

    >>> for i in range(200):
    ...     n = 123 ** i
    ...     assert isqrt(n) ** 2 <= n < (isqrt(n) + 1) ** 2
    """
    try:
        y = int(_math.sqrt(n) * 1.01)
    except OverflowError:
        return _isqrtd(n)
        # y = (n + 1) // 2
    x = y + 1
    while y < x:
        x, y = y, (y + n // y) // 2
    return x


def average(items):
    """
    Return the average of the items.

    >>> average(range(10))
    4.5
    """
    items = iter(items)
    try:
        total_sum = next(items)
    except StopIteration:
        return ValueError('average of 0 items undefined.')
    cnt = 1
    for item in items:
        cnt += 1
        total_sum += item

    return total_sum / cnt
