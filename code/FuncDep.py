import sqlite3

class FuncDep:
    def __init__(self, other):
        self.data = other
        if 'FuncDep' in self.data.printTables():
            print('ok')
        else:
            self.data.db.execute('''CREATE TABLE FuncDep (
            table_name VARCHAR(10) NOT NULL,
            lhs VARCHAR(20) NOT NULL,
            rhs VARCHAR(10) NOT NULL
            ) ''')
            self.data.db.commit()

