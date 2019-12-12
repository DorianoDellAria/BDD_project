import sqlite3
import FuncDep

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.df = []

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

    def addFuncDep(self, tableName, lhs, rhs):
        self.df += [FuncDep.FuncDep(tableName,lhs,rhs),]

        if 'FuncDep' not in self.printTables():
            self.db.execute('''CREATE TABLE FuncDep (
            table_name VARCHAR(10) NOT NULL,
            lhs VARCHAR(20) NOT NULL,
            rhs VARCHAR(10) NOT NULL
            ) ''')
            self.db.commit()
        tmp = 'INSERT INTO FuncDep VALUES (?,?,?);'
        self.db.execute(tmp,(tableName,lhs,rhs))
        self.db.commit()
        


if __name__ == "__main__":
    test = DataBase('tables.db')
    print(test.printTables())
    print(test.printColumn('dept'))
    test.close()