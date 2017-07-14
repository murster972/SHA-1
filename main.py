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

        #padds m
        padded = self.padd()

        #splits m into 512-but blocks
        x_values = [padded[i - 512:i] for i in range(512, len(padded) + 1, 512)]

        #inital hash value
        h = ["67452301", "EFCDAB89", "98BADCFE", "10325476", "C3D2E1F0"]
        h = [bin(int(i, 16))[2:] for i in h]
        h = [("0" * (32 - len(i))) + i for i in h]
        h0, h1, h2, h3, h4 = tuple(h)

        keys = ["5A827999", "6ED9EBA1", "8F1BBCDC", "CA62C1D6"]
        keys = [bin(int(i, 16))[2:] for i in keys]
        keys = [("0" * (32 - len(i))) + i for i in keys]

        #80-rounds for each 512-bit value
        for x in x_values:
            #80 32-bit words used in the 80 rounds
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

            a, b, c, d, e = h0, h1, h2, h3, h4

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
                tmp = ("0" * (32 - len(tmp))) + tmp
                a = tmp

                #NOTE: may not be an XOR sum
                #NOTE: Its not a fucking XOR SUM, silly cunt...

            a = bin((int(a, 2) + int(h0, 2)) % pow(2, 32))[2:]
            b = bin((int(b, 2) + int(h1, 2)) % pow(2, 32))[2:]
            c = bin((int(c, 2) + int(h2, 2)) % pow(2, 32))[2:]
            d = bin((int(d, 2) + int(h3, 2)) % pow(2, 32))[2:]
            e = bin((int(e, 2) + int(h4, 2)) % pow(2, 32))[2:]

            abcde = [a, b, c, d, e]

            for i in range(5):
                abcde[i] = ("0" * (32 - len(abcde[i]))) + abcde[i]

            h0, h1, h2, h3, h4 = tuple(abcde)

        h = h0 + h1 + h2 + h3 + h4

        print(hex(int(h, 2))[2:])
        #return hex(int(h, 2))[2:]

    def f_t(self, t, b, c, d):
        #NOTE: second value of b has line above it in book, may mean something
        #NOTE: It means the inverse of b you cunt...
        b_inverse = "".join(["0" if i == "1" else "1" for i in b])

        if t < 20: r = (int(b, 2) & int(c, 2)) | (int(b_inverse, 2) & int(d, 2))
        elif t < 40: r = int(b, 2) ^ int(c, 2) ^ int(d, 2)
        elif t < 60: r = (int(b, 2) & int(c, 2)) | (int(b, 2) & int(d, 2)) | (int(c, 2) & int(d, 2))
        else: r = int(b, 2) ^ int(c, 2) ^ int(d, 2)

        r_bin = bin(r)[2:]

        return ("0" * (32 - len(r_bin))) + r_bin

    def padd(self):
        bin_m = [bin(ord(i))[2:] for i in self.m]
        bin_m = [("0" * (8 - len(i))) + i for i in bin_m]

        l = len(bin_m) * 8
        l_bin_padd = 64 - int(math.floor(math.log(l, 2)) + 1)

        if l_bin_padd < 0:
            raise Exception("m cannot more than 2**64 bits in length")

        k = (448 - (l + 1)) % 512

        padd_m = "".join(bin_m) + "1" + ("0" * k)
        padd_m += ("0" * l_bin_padd) + bin(l)[2:]

        return padd_m

    def circular_shift(self, b, x):
        t = b
        for i in range(x): t = t[1:] + t[0]
        return t

if __name__ == '__main__':
    SHA1().get_hash("abwekfnlkm;lwefijowneimf;klc")
