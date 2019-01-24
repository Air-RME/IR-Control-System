# coding: utf-8

import json
from collections import Counter
import csv
import sys

# default
args = sys.argv  # [0]=読み込みファイル[1]=コマンド名
jsonFile_Name = 'temp.json'

# export
writer = csv.writer(open('_ir-hex-codes.csv', 'a', newline=''))
subwriter = csv.writer(open('ir-analytics.csv', 'a', newline=''))


# 単位時間Tの算出
def getPulseSecPattern(jsonFile_Name, command_Name):
    ir_PulseList = getJsonData(jsonFile_Name)[command_Name]
    value, count = zip(*Counter(ir_PulseList).most_common(1))
    T = value[0]
    T8 = ir_PulseList[0]
    true_T = (T8 - T) / 7

    print('command= %s' % (command_Name))
    print('T= %d' % (value[0]))
    print('8T= %d' % (ir_PulseList[0]))
    print('true_T= %d' % (true_T))
    return true_T


def getJsonData(jsonFile_Name):
    file = open(jsonFile_Name, 'r')
    jsonData = json.load(file)
    file.close()
    return jsonData


def reverse_bit8(x):
    x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
    x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
    return ((x & 0x0F) << 4 | x >> 4)


def reverse_bit4(x):
    x = ((x & 0x5) << 1) | ((x & 0xA) >> 1)
    x = ((x & 0x3) << 2) | ((x & 0xC) >> 2)
    return x


def ir_codes_WriteHexCsv(jsonFile_Name, command_Name):
    file = open(jsonFile_Name, 'r')
    jsonData = json.load(file)[command_Name]
    T = getPulseSecPattern(jsonFile_Name, command_Name)
    reader = jsonData

    # initialize
    data_counter = 0
    leader_flag = 0

    for row in reader:
        # detect pulse length
        length = int(round(int(row) / T))

        # detect leader
        if length == 8:
            leader_flag = 1  # 8length pulse detect

        # init frame
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
                # pulse_flag off
                pulse_flag = 0
                # detect bit on/off/tracer
                if length == 1:
                    bit = 0
                elif length == 3:
                    bit = 1
                else:
                  # data_str = [hex(x) for x in frame]
                    data_str = [x for x in frame]
                    total = 0
                    for num in range(13):
                        total = total + data_str[num]
                    writer.writerow([command_Name])
                    data_str = [x for x in frame]
                    writer.writerow([total])
                    writer.writerow(data_str)
                    writer.writerow([''])
                    writer.writerow(["tracer"])

                    subwriter.writerow([total,data_str[13]])

                datum = datum << 1 | bit

                # detect 4bit datum(parity, data0)
                if data_counter == 20 or data_counter == 24:
                    frame.append(reverse_bit4(datum))
                    datum = 0
                # detect 8bit datum(customer, data1~)
                elif data_counter % 8 == 0:
                    frame.append(reverse_bit8(datum))
                    datum = 0

    # data_str = [hex(x) for x in frame]
    data_str = [x for x in frame]
    total = 0
    for num in range(13):
        total = total + data_str[num]
    writer.writerow([command_Name])
    data_str = [x for x in frame]
    writer.writerow([total])
    writer.writerow(data_str)
    writer.writerow([''])

    subwriter.writerow([total,data_str[13]])

# main　引数なしの場合ファイル全てのコマンドを読み込み変換
if (len(args) == 3):#引数あり　ファイル名とコマンド名
    jsonFile_Name = args[1]
    command_Name = args[2]
    ir_codes_WriteHexCsv(jsonFile_Name, command_Name)
elif (len(args) == 2):#引数あり　ファイル名のみ
    keyList = getJsonData(args[1]).keys()
    for key in keyList:
        ir_codes_WriteHexCsv(args[1], key)
else:
    keyList = getJsonData(jsonFile_Name).keys()
    for key in keyList:
        ir_codes_WriteHexCsv(jsonFile_Name, key)
