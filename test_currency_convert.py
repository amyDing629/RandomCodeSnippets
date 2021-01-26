#!/usr/bin/env python3
import unittest
import pandas as pd
from currency_convert import currency_convert


class test_currency_convert(unittest.TestCase):
    def test_currency_convert1(self):
        currency_convert("Price Per Month", 5, "mydata.csv", "newdata1.csv")
        df1 = pd.read_csv("mydata.csv")
        df2 = pd.read_csv("newdata1.csv")
        assert(len(df1) == len(df2))
        assert(len(df1["Feed Name"]) == len(df2["Feed Name"]))
        assert(df2["Price Per Month"][1] == "\u20ac 275,60")
        assert(df2["Price Per Month"][2] == "\u20ac 4130,10")

    def test_currency_convert2(self):
        currency_convert("Price Per Month", 0.8, "mydata.csv", "newdata2.csv")
        df2 = pd.read_csv("newdata2.csv")
        assert (df2["Price Per Month"][0] == "\u20ac 59,38")
        assert (df2["Price Per Month"][2] == "\u20ac 660,82")
        assert (df2["Price Per Month"][4] == "\u20ac 15,70")



if __name__ == '__main__':
    unittest.main()