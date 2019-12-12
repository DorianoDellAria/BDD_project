import sqlite3

class FuncDep:
    def __init__(self, tableName, lhs, rhs):
        self.tableName = tableName
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "<"+self.tableName +",("+ self.lhs+")," + self.rhs+">"
            


    

    