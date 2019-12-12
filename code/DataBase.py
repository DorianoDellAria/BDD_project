import sqlite3
import FuncDep

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.df = FuncDep.FuncDep(self)

    def printTables(self):
        cursor = self.db.execute("SELECT * FROM sqlite_master WHERE type='table'")
        chain = []
        for i in cursor:
            chain += [i[2],]
        return chain

    def printColumn(self, table):
        cursor = self.db.execute("SELECT * FROM " + table)
        return list(map(lambda x: x[0],cursor.description))

    def close(self):
        self.db.close()
        print("\ndata base closed")
        


if __name__ == "__main__":
    test = DataBase('tables.db')
    print(test.printTables())
    print(test.printColumn('dept'))
    test.close()