#!/usr/bin/python3

import argparse
import DataBase
import command

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("table")
    args = parser.parse_args()

    test = DataBase.DataBase(args.table)
    
    cmd = command.command(test)
    cmd.cmdloop()

if __name__ == "__main__":
    main()
    
    