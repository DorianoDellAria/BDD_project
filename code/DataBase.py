import sqlite3
import FuncDep
from copy import deepcopy

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.df = []
        if 'FuncDep' in self.getTables():
            cursor = self.db.execute('SELECT * FROM FuncDep;')
            for t in cursor:
                self.df += [FuncDep.FuncDep(t[0],t[1],t[2],self.db),]

    def getTables(self):
        cursor = self.db.execute("SELECT * FROM sqlite_master WHERE type='table'")
        chain = []
        for i in cursor:
            chain += [i[2],]
        return chain

    def getColumn(self, table):
        if table not in self.getTables():
            return "this table doesn't exist"
        cursor = self.db.execute("SELECT * FROM " + table)
        return list(map(lambda x: x[0],cursor.description))

    def close(self):
        self.db.close()
        print("\ndata base closed")

    def addFuncDep(self, tableName, lhs, rhs):
        if 'FuncDep' not in self.getTables():
            self.db.execute('''CREATE TABLE FuncDep (
            table_name VARCHAR(10) NOT NULL,
            lhs VARCHAR(20) NOT NULL,
            rhs VARCHAR(10) NOT NULL
            ) ''')
            self.db.commit()
        
        """condition d'existance de table"""
        if tableName not in self.getTables():
            print("this table doesn't exit")
            return

        """condition d'existance de la gauche"""
        for i in lhs.split(','):
            if i not in self.getColumn(tableName):
                print("lhs : this column doesn't exist")
                return
        
        """condition d'existance de la droite"""
        if rhs not in self.getColumn(tableName):
            print("rhs : this column doesn't exist")
            return
        

        tmp = 'INSERT INTO FuncDep VALUES (?,?,?);'
        self.db.execute(tmp,(tableName,lhs,rhs))
        self.db.commit()
        self.df += [FuncDep.FuncDep(tableName,lhs,rhs,self.db),]
    
    def getFD(self):
        chain =''
        for i in range(len(self.df)):
            chain+=str(i) + " : "+ str(self.df[i])
            chain+='\n'
        return chain

    def removeFuncDep(self,number):
        if number == -1:
            print(self.getFD())
            number = int(input("which one do you want to remove ? : "))

        if len(self.df) == 0 or number < 0 or number >= len(self.df):
            print("this FD doesn't exist")
            return
        
        self.db.execute("DELETE FROM FuncDep where table_name = ? and lhs = ? and rhs = ?;",(self.df[number].tableName,self.df[number].lhs,self.df[number].rhs))
        self.db.commit()
        self.df.pop(number)
    
    def checkFD(self):
        for i in self.df:
            print(i, " : ", i.check())

    def closure(self, X:str, F:list, table :str)->list:
        olddep = []
        newdep = [X]
        while olddep != newdep:
            olddep = newdep
            for i in F:
                if table == i.tableName and i.lhs in newdep:
                    newdep += [i.rhs,]
        return newdep


    #pas bon
    # def cons(self,table):
    #     tmp = deepcopy(self.df)
    #     for i in range(len(tmp)):
    #         t1 = self.closure(tmp[i].lhs, tmp, table)
    #         tmp2 = deepcopy(tmp)
    #         tmp2.pop(i)
    #         t2 = self.closure(tmp[i].lhs, tmp, table)
    #         if t1 == t2:
    #             print(tmp[i])


if __name__ == "__main__":
    test = DataBase('tables.db')
    print(test.getTables())
    print(test.getColumn('dept'))
    test.close()