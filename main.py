#!/usr/bin/env python3
import sys
import math

#NOTE: IT FUCKING WORKS NOW :D
#NOTE: The reason for it initally producing an incorrect hash values:
#       Using an XOR sum instead mod 2**32 when adding values during rounds
#       The second B value in the first round function was not inversed

class SHA1:
    def get_hash(self, m):
        self.m = m

        if not self.m: raise Exception("m cannot be an empty.")

        padded = self.padd()

        x_values = [padded[i - 512:i] for i in range(512, len(padded) + 1, 512)]

        h = ["67452301", "EFCDAB89", "98BADCFE", "10325476", "C3D2E1F0"]
        h = [self.padd_bin(bin(int(i, 16))[2:]) for i in h]

        keys = ["5A827999", "6ED9EBA1", "8F1BBCDC", "CA62C1D6"]
        keys = [self.padd_bin(bin(int(i, 16))[2:]) for i in keys]

        for x in x_values:
            words = []

            for i in range(32, 2561, 32):
                if i // 32 <= 16:
                    words.append(x[i - 32:i])
                else:
                    j = i // 32 - 1
                    w = [words[j - 16], words[j - 14], words[j - 8], words[j - 3]]
                    word = ""

                    for i in range(32): word += str(sum([int(s[i]) for s in w]) % 2)

                    words.append(word[1:] + word[0])

            a, b, c, d, e = tuple(h)

            for i in range(80):
                f = self.f_t(i, b, c, d)
                if i < 20: k = keys[0]
                elif i < 40: k = keys[1]
                elif i < 60: k = keys[2]
                else: k = keys[3]

                tmp = e
                b, c, d, e = a, self.circular_shift(b, 30), c, d

                tmp = [tmp, f, self.circular_shift(a, 5), words[i], k]
                tmp = bin(sum([int(i, 2) for i in tmp]) % pow(2, 32))[2:]
                a = self.padd_bin(tmp)

            reg = [a, b, c, d, e]

            for i in range(5):
                n = bin((int(reg[i], 2) + int(h[i], 2)) % pow(2, 32))[2:]
                reg[i] = self.padd_bin(n)

            h = [] + reg

        return hex(int("".join(reg), 2))[2:]

    def f_t(self, t, b, c, d):
        b_inverse = int("".join(["0" if i == "1" else "1" for i in b]), 2)
        b_i, c_i, d_i = int(b, 2), int(c, 2), int(d, 2)

        if t < 20: r = (b_i & c_i) | (b_inverse & d_i)
        elif t < 40 or (t > 59 and t < 80): r = b_i ^ c_i ^ d_i
        else: r = (b_i & c_i) | (b_i & d_i) | (c_i & d_i)

        return self.padd_bin(bin(r)[2:])

    def padd(self):
        bin_m = [self.padd_bin(bin(ord(i))[2:], 8) for i in self.m]

        l = len(bin_m) * 8
        l_bin_padd = 64 - int(math.floor(math.log(l, 2)) + 1)

        if l_bin_padd < 0: raise Exception("m cannot more than 2**64 bits in length")

        k = (448 - (l + 1)) % 512

        padd_m = "".join(bin_m) + "1" + ("0" * k)
        padd_m += ("0" * l_bin_padd) + bin(l)[2:]

        return padd_m

    def circular_shift(self, b, x):
        t = b
        for i in range(x): t = t[1:] + t[0]
        return t

    def padd_bin(self, v, l=32):
        return ("0" * (l - len(v))) + v

if __name__ == '__main__':
    m = "7398029-r0[lp2,3lrmkpni2-3or[p23rm]]"
    h = SHA1().get_hash(m)
    print(h)
