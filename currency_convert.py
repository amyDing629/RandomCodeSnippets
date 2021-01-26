#!/usr/bin/env python3
import argparse
import sys
import test_currency_convert


def usd_to_euro(num, multiplier):
    return "\"" + '\u20ac ' + str('%.2f' % (float(num) * multiplier)).replace(".", ",") + "\""


def currency_convert(field, multiplier, input_f, output_f):
    # read csv files
    lst = []
    if input_f == "":
        for line in sys.stdin:
            if 'q' == line.rstrip():
                break
            lst.append(line.split(","))
            print("append success")
    else:
        with open(input_f) as file:
            for line in file:
                lst.append(line.split(","))

    num = -1
    # modify csv files
    for i in range(len(lst[0])):
        if lst[0][i] == field:
            num = i
    if num == -1:
        print("Error: field not existed")
    else:
        for sublist in lst[1:]:
            sublist[num] = usd_to_euro(sublist[num], multiplier)
    # for a list of lines
    rst_lst = []
    for sublist in lst:
        line = ""
        for element in sublist:
            line += (str(element) + ",")
        rst_lst.append(line)
    # write csv files
    if output_f == "":
        for line in rst_lst:
            print(line[:-1])
    else:
        file2 = open(output_f, "w")
        for line in rst_lst:
            file2.write(line[:-1])
        file2.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--field", metavar='N', help="Convert CSV field N", type=str, required=True)
    parser.add_argument("--multiplier", metavar='N',
                        help="Multiply currency values by N for the current conversion rate",
                        type=float, default=1)
    parser.add_argument("-i", metavar='input', help="Read from input file (or stdin)", type=str, default="")
    parser.add_argument('-o', metavar='output', help="Write to output file (or stdout)", type=str, default="")
    args = parser.parse_args()
    currency_convert(args.field, args.multiplier, args.i, args.o)


if __name__ == "__main__":
    main()
