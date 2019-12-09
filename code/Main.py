#!/usr/bin/python3

import argparse
import DataBase

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("table")
    args = parser.parse_args()

    test = DataBase.DataBase(args.table)
    print(test.printTables())
    print(test.printColumn('dept'))
    test.close()

if __name__ == "__main__":
    main()