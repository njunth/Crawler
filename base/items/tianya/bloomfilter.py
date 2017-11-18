
#-*-coding:utf8-*-


import cmath
from BitVector import BitVector


class BloomFilter(object):
    def __init__(self, error_rate, elementNum):

        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))

        self.bit_num = self.align_4byte(self.bit_num.real)

        self.bit_array = BitVector(size=self.bit_num)

        self.hash_num = cmath.log(2) * self.bit_num / elementNum

        self.hash_num = self.hash_num.real

        self.hash_num = int(self.hash_num) + 1

        self.hash_seeds = self.generate_hashseeds(self.hash_num)

    def insert_element(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)

            hash_val = abs(hash_val)

            hash_val = hash_val % self.bit_num

            self.bit_array[hash_val] = 1

    def is_element_exist(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)

            hash_val = abs(hash_val)

            hash_val = hash_val % self.bit_num

            if self.bit_array[hash_val] == 0:
                return False
        return True

    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num

    def generate_hashseeds(self, hash_num):
        count = 0

        gap = 50

        hash_seeds = []
        for index in xrange(hash_num):
            hash_seeds.append(0)
        for index in xrange(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in xrange(2, max_num):
                if index % num == 0:
                    flag = 0
                    break

            if flag == 1:

                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count = count + 1

            if count == hash_num:
                break
        return hash_seeds

    def hash_element(self, element, seed):
        hash_val = 1
        for ch in str(element):
            chval = ord(ch)
            hash_val = hash_val * seed + chval
        return hash_val
