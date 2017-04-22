#!/usr/bin/env python3
import os
import sys

#BUG: Hash values not the same as hash vals generated online,
#     unsure why, go through and check algo matches SHA-1 algo.
#BUG: POSSIBLE: Bitwsie operations not behaving correctly when going
#     from binary string or hex string to int

class SHA1:
    def sha1(self, msg):
        self.m = "".join(["0" + str(bin(ord(x)))[2:] for x in msg])
        self.block_padding()
        blocks = [self.m[x - 512:x] for x in range(512, len(self.m) + 1, 32)]

        H = ("67452301", "EFCDAB89", "98BADCFE", "10325476", "C3D2E1F0")

        for b in blocks:
            w = self.msg_schedule(b)
            a, b, c, d, e = H

            for i in range(0, 80):
                if i <= 19: k = ("5A827999", 1)
                elif i <= 39: k = ("6ED9EBA1", 2)
                elif i <= 59: k = ("8F1BBCDC", 3)
                elif i <= 79: k = ("CA62C1D6", 4)

                a1, b1, c1, d1, e1 = a, b, c, d, e
                a = self.function_t(b1, c1, d1, k[1])
                print(b1, c1, d1, k[1])
                print(a)
                a = (int(a, 2) + int(e1, 16)) % 2**32
                a = (a + int(self.circular_shift(a1, 5), 16)) % 2**32
                a = (a + int(w[i], 2)) % 2**32
                a = self.padd((a + int(k[0], 16)) % 2**32)
                a = self.to_hex(a)

                b = a1
                c = self.circular_shift(b1, 30)
                d = c1
                e = d1

            a = self.padd((int(a, 16) + int(H[0], 16)) % 2**32)
            c = self.padd((int(c, 16) + int(H[1], 16)) % 2**32)
            b = self.padd((int(b, 16) + int(H[2], 16)) % 2**32)
            d = self.padd((int(d, 16) + int(H[3], 16)) % 2**32)
            e = self.padd((int(e, 16) + int(H[4], 16)) % 2**32)
            H = self.to_hex(a), self.to_hex(b), self.to_hex(c), self.to_hex(d), self.to_hex(e)
        return "".join(H)

    def block_padding(self):
        l = str(bin(len(self.m)))[2:]
        k = ((447 - int(l, 2)) % 512 + 512) % 512
        self.m += "1" + ("0" * k) + ("0" * (64 - len(l))) + l

    def padd(self, x):
        x = str(bin(x))[2:]
        return ("0" * (32 - len(x))) + x

    def msg_schedule(self, b):
        w = [b[x - 32:x] for x in range(32, len(b) + 1, 32)]

        for j in range(16, 80):
            tmp = int(w[j - 16], 2) ^ int(w[j - 14], 2) ^ int(w[j - 8], 2) ^ int(w[j - 3], 2)
            tmp = self.padd(tmp)
            w.append(tmp[1:] + tmp[0])
        return w

    def function_t(self, b, c, d, t):
        if t == 1:
            x = (int(b, 16) & int(c, 16)) | (int(b, 16) & int(d, 16))
        #BUG: not returning correct value, unkown why
        elif t == 2 or t == 4:
            x = int(b, 16) ^ int(c, 16) ^ int(d, 16)
        elif t == 3:
            x = (int(b, 16) & int(c, 16)) | (int(b, 16) & int(d, 16)) | (int(c, 16) & int(d, 16))
        return self.padd(x)

    def circular_shift(self, x, shift):
        x1 = self.padd(int(x, 16))
        for i in range(0, shift):
            x1 = x1[1:] + x1[0]
        return self.to_hex(x1)

    def to_hex(self, h):
        #return str(hex(int(h, 2)))[2:]
        x = [h[i - 4:i] for i in range(4, len(h) + 1, 4)]
        hex_vals = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
        h_val = ""
        for b in x:
            i = int(b, 2)
            h_val += str(i) if i < 10 else hex_vals[i]
        return h_val

if __name__ == '__main__':
    msg = "abc"
    #hash_val = SHA1().function_t("EFCDAB89", "98BADCFE", "10325476", 4)
    hash_val = SHA1().sha1(msg)
    print(hash_val)
