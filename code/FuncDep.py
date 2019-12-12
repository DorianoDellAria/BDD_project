import sqlite3

class FuncDep:
    def __init__(self, other):
        self.data = other
            


    def addFuncDep(self, tableName, lhs, rhs):
        if 'FuncDep' not in self.data.printTables():
            self.data.db.execute('''CREATE TABLE FuncDep (
            table_name VARCHAR(10) NOT NULL,
            lhs VARCHAR(20) NOT NULL,
            rhs VARCHAR(10) NOT NULL
            ) ''')
            self.data.db.commit()
        
        self.data.db.execute("INSERT INTO FuncDep VALUES (" + tableName + "," + lhs + "," + rhs+");")
        self.data.db.commit()

    