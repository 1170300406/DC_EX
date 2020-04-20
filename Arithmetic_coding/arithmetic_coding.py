# coding=utf-8
"""
Created on 2020/3/30 17:50
By cfsfine

"""
from collections import Counter


class ArithmaticCoding:

    def __init__(self):
        self.ptable = {}

    def compress(self, word):
        word_list = list (word)
        table = Counter (word_list)
        total = len (word_list)
        sum = 0
        for k in table.keys ():
            self.ptable[k] = (sum, sum + table[k] / total)
            sum += table[k] / total

        low = 0
        high = 1
        low_list = []
        high_list = []

        for w in word_list:
            flag = 0
            if low == 0 or high == 1:
                old_low = low
                low = old_low + (high - old_low) * self.ptable[w][0]
                high = old_low + (high - old_low) * self.ptable[w][1]
                low_list = list (str (low))
                high_list = list (str (high))
            else:
                for i in range (len (low_list)):
                    if low_list[i] == high_list[i]:
                        flag += 1
                        continue
                    else:
                        break
                low = float ("0." + "".join (low_list[flag:]))
                high = float ("0." + "".join (high_list[flag:]))
                old_low = low
                low = old_low + (high - old_low) * self.ptable[w][0]
                high = old_low + (high - old_low) * self.ptable[w][1]
                for i in range (len (low_list) - flag):
                    low_list.pop ()
                for i in range (len (high_list) - flag):
                    high_list.pop ()
                temp_low = list (str (low)[2:])
                temp_high = list (str (high)[2:])
                low_list += temp_low
                high_list += temp_high
        return high_list

    def decompress(self, code_list):
        result_list = []
        decompress_section = {}
        for k in self.ptable.keys ():
            decompress_section[k] = (list (str (self.ptable[k][0])), list (str (self.ptable[k][1])))
        high_result_list = ['1']
        while True:
            find = 0
            for k in decompress_section.keys ():
                low_list = decompress_section[k][0]
                high_list = decompress_section[k][1]
                high_result_list = high_list
                if low_list == ['0'] or low_list == ['0', '.', '0']:
                    index = 0
                    while True:
                        h = high_list[index]
                        c = code_list[index]
                        if h == c:
                            if index != len (code_list) - 1:
                                index += 1
                            else:
                                find = 1
                                break
                            continue
                        elif h > c:
                            find = 1
                            break
                        else:
                            break
                elif high_list == ['1'] or high_list == ['1', '.', '0']:
                    index = 0
                    while True:
                        l = low_list[index]
                        c = code_list[index]
                        if l == c:
                            index += 1
                            continue
                        elif l > c:
                            break
                        else:
                            find = 1
                            break
                else:
                    index = 0
                    find1 = 0
                    while True:
                        h = high_list[index]
                        c = code_list[index]
                        if h == c:
                            if index != len (code_list) - 1:
                                index += 1
                            else:
                                find = 1
                                break
                            continue
                        elif h > c:
                            find1 = 1
                            break
                        else:
                            break
                    index = 0
                    if find1 == 1:
                        while True:
                            l = low_list[index]
                            c = code_list[index]
                            if h == c:
                                index += 1
                                continue
                            elif l > c:
                                break
                            else:
                                find = 1
                                break
                if find == 1:
                    result_list.append (k)

                    low = float ("".join (low_list))
                    high = float ("".join (high_list))
                    if low == 0 or high == 1:
                        old_low = low
                        old_high = high
                        for ki in self.ptable.keys ():
                            low = old_low + (old_high - old_low) * self.ptable[ki][0]
                            high = old_low + (old_high - old_low) * self.ptable[ki][1]
                            low_temp_list = list (str (low))
                            high_temp_list = list (str (high))
                            decompress_section[ki] = (low_temp_list, high_temp_list)
                    else:
                        flag = 0
                        for i in range (len (low_list)):
                            if low_list[i] == high_list[i]:
                                flag += 1
                                continue
                            else:
                                break
                        low = float ("0." + "".join (low_list[flag:]))
                        high = float ("0." + "".join (high_list[flag:]))
                        old_low = low
                        old_high = high
                        for w in self.ptable.keys ():
                            low_temp_list = low_list.copy ()
                            high_temp_list = high_list.copy ()
                            low = old_low + (old_high - old_low) * self.ptable[w][0]
                            high = old_low + (old_high - old_low) * self.ptable[w][1]
                            for i in range (len (low_list) - flag):
                                low_temp_list.pop ()
                            for i in range (len (high_list) - flag):
                                high_temp_list.pop ()
                            temp_low = list (str (low)[2:])
                            temp_high = list (str (high)[2:])
                            low_temp_list += temp_low
                            high_temp_list += temp_high
                            decompress_section[w] = (low_temp_list, high_temp_list)
                    break
                else:
                    continue
            max_flag = 7
            flag1 = 0
            flag2 = 0
            while True:
                c = code_list[flag1]
                h = high_result_list[flag1]
                if c == h and c != '0':
                    if flag1 != len (code_list) - 1:
                        flag1 += 1
                        flag2 = 0
                    else:
                        flag2 = 8
                        break
                    continue
                elif c == h and c == '0':
                    flag1 += 1
                    flag2 += 1
                    if flag2 > max_flag:
                        break
                else:
                    break
            if flag2 > max_flag:
                break
        return result_list


if __name__ == '__main__':
    a = ArithmaticCoding ()
    s = 'ARBEREREEBAAAAAAAAAAAERAEARAEAREARAEARAEAABBBBBBBBBBBBEEEEEEEAAARERERERARARARARARERARERAERAER'
    b = a.compress (s)
    print (''.join (b))
    print (''.join (a.decompress (b)))
    print (''.join (a.decompress (b)) == s)
