import itertools
import string

from collections import namedtuple

from random import choices, randint

alphabet = string.ascii_lowercase


def erat():
    D = {}
    yield 2
    for q in itertools.islice(itertools.count(3), 0, None, 2):

        p = D.pop(q, None)
        if p is None:
            D[q * q] = q
            yield q

        else:
            x = p + q
            while x in D or not (x & 1):
                x += p
            D[x] = p


def get_number_primes(n):
    primes_number = list(itertools.takewhile(lambda p: p < n, erat()))
    return primes_number


def create_key_dh(n):
    prime_list_number = get_number_primes(n)
    p = choices(prime_list_number, k=1)[0]

    g = randint(2, p - 1)
    x = randint(2, p - 1)
    y = pow(g, x, p)

    keys = namedtuple("keys", "p g y")

    public = keys(p, g, y)
    private = x
    return p, public, private


def encryption(m, p, public):
    k = randint(2, p - 1)
    a = pow(public.g, k, p)
    b = pow(m * pow(public.y, k), 1, p)
    return a, b


def decryption(x, a, b, p):
    m = pow(b * pow(a, p - 1 - x), 1, p)
    return m


if __name__ == "__main__":
    p, public_key, private_key = create_key_dh(2 ** 20)
    print("Наберіть повідомлення:")

    message_text = int(input())

    a, b = encryption(message_text, p, public_key)
    print(f"Зашифрований текст: {a, b}")

    text_decoded = decryption(private_key, a, b, p)
    print(f"Дешифрований текст: {text_decoded}")
