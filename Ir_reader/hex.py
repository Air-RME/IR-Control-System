# coding: utf-8

import json
from collections import Counter


def reverse_bit8(x):
    x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
    x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
    return ((x & 0x0F) << 4 | x >> 4)


def reverse_bit4(x):
    x = ((x & 0x5) << 1) | ((x & 0xA) >> 1)
    x = ((x & 0x3) << 2) | ((x & 0xC) >> 2)
    return x


def ir_codes_conversion(pulseList):
    ir_PulseList = pulseList
    value, count = zip(*Counter(ir_PulseList).most_common(1))
    T = value[0]
    T8 = ir_PulseList[0]
    true_T = (T8 - T) / 7

    T = true_T

    reader = ir_PulseList

    # initialize
    data_counter = 0
    leader_flag = 0

    for row in reader:
        # detect pulse length
        length = int(round(int(row) / T))
        # detect leader
        if length == 8:
            leader_flag = 1  # 8length pulse detect
        if length == 4 and leader_flag == 1:
            leader_flag = 2  # leader_detect
            data_counter = 0
            frame = []
            datum = 0
            pulse_flag = 0
        # detect frame
        if leader_flag == 2:
            if length == 1 and pulse_flag == 0:
                data_counter = data_counter + 1
                pulse_flag = 1
            elif pulse_flag:
                # print (data_counter, length)
                # pulse_flag off
                pulse_flag = 0
                # detect bit on/off/tracer
                if length == 1:
                    bit = 0
                elif length == 3:
                    bit = 1
                else:
                    pass

                datum = datum << 1 | bit

                # detect 4bit datum(parity, data0)
                if data_counter == 20 or data_counter == 24:
                    frame.append(reverse_bit4(datum))
                    datum = 0
                # detect 8bit datum(customer, data1~)
                elif data_counter % 8 == 0:
                    frame.append(reverse_bit8(datum))
                    datum = 0

    data_str = [bin(x) for x in frame]
    return data_str
