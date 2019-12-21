import sqlite3
import FuncDep
from copy import deepcopy
from random import shuffle

class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.df = []
        if 'FuncDep' in self.getTables():
            cursor = self.db.execute('SELECT * FROM FuncDep;')
            for t in cursor:
                self.df += [FuncDep.FuncDep(t[0],t[1],t[2]),]

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
        for i in lhs.split(' '):
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
        self.df += [FuncDep.FuncDep(tableName,lhs,rhs),]
    
    def getFD(self, table=None):
        chain =''
        for i in range(len(self.df)):
            if table==None or table==self.df[i].tableName:
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
            print(i, " : ", i.check(self))

    def closure(self, X:str, F:list, table :str)->list:
        olddep = []
        newdep = X.split(' ')
        while olddep != newdep:
            olddep= deepcopy(newdep)
            for i in F:
                if ' ' in i.lhs and table == i.tableName:
                    tmp=i.lhs.split(' ')
                    b=True
                    for j in tmp:
                        if j not in newdep:
                            b=False
                            break
                    if b and i.rhs not in newdep:
                        newdep += [i.rhs,]
                        continue
                if table == i.tableName and (i.lhs in newdep) and (i.rhs not in newdep):
                    newdep += [i.rhs,]
        return newdep


    def cons(self,table):
        tmp = deepcopy(self.df)
        b=True
        res = []
        while b:
            b=False
            for i in range(len(tmp)):
                if tmp[i].tableName != table:
                    continue
                t1 = self.closure(tmp[i].lhs, tmp, table)
                tmp2 = deepcopy(tmp)
                tmp2.pop(i)
                t2 = self.closure(tmp[i].lhs, tmp2, table)
                b=True
                for j in t1:
                    if j not in t2:
                        b=False
                        break
                if b:
                    print(tmp[i])
                    res += [tmp.pop(i),]
                    b=True
                    break
        return res
            
    def sKey(self, table):
        column = self.getColumn(table)
        obvious = ''
        toComp=[]
        '''Finding obvious element'''
        for element in column:
            test = True
            for i in self.df:
                if element == i.rhs and table==i.tableName:
                    test=False
                    toComp+=[element,]
                    break
            if test:
                if obvious == '':
                    obvious+=element
                else:
                    obvious+=' '+element
        # print(obvious)
        #end of finding obvious element
        if include( self.getColumn(table) ,self.closure(obvious,self.df,table)):
            return obvious
        else:
            candidate=[]
            for i in range(1,len(toComp)+1):
                candidate += list(choose_iter(toComp,i))
            candidate = refact(candidate,obvious)
            sKey=[]
            for i in candidate:
                if include(self.getColumn(table),self.closure(i,self.df,table)):
                    sKey+=[i,]
        return self.key(sKey,obvious)

    def key(self,sKey:list,chain:str):
        for i in range(len(sKey)):
            sKey[i] = sKey[i].replace(chain,'')
        result = deepcopy(sKey)
        for loop in range(len(sKey)):
            copy = deepcopy(result)
            for i in range(len(sKey)):
                for j in range(len(sKey)):
                    if i==j:
                        continue
                    if include(sKey[j].split(),sKey[i].split()) and sKey[i] in result and len(sKey[i].split())>len(sKey[j].split()):
                        result.remove(sKey[i])
                        i-=1
                        break
            if copy==result:
                break
        for i in range(len(result)):
            result[i] = result[i] + chain
        return result
    
    def checkBCNF(self, table:str)->bool:
        keys = self.sKey(table)
        for i in self.df:
            if i.tableName==table and not i.lhs in keys:
                return False
        return True
    
    def check3NF(self,table:str)->bool:
        if self.checkBCNF(table):
            return True
        else:
            keys = self.sKey(table) 
            for i in self.df:
                if i.tableName==table and (i.lhs not in keys) and (not includeInKey(i.rhs,keys)):
                    return False
            return True
                
                    

                    





def includeInKey(rhs:str,keys:list)->bool:
    for i in keys:
        if rhs in i.split():
            return True
    return False


def include(a:list,b:list)->bool:
    for i in a:
        if i not in b:
            return False
    return True

# https://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n
def choose_iter(elements, length):
    for i in range(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i+1:len(elements)], length-1):
                yield (elements[i],) + next

def refact(arr:list,chain:str):
    result=[]
    for i in arr:
        tmp = ''
        for j in range(len(i)-1):
            tmp+=str(i[j])+' '
        tmp += str(i[len(i)-1])
        if chain != '':
            tmp += ' '+ chain
        result+=[tmp,]
    return result
            



if __name__ == "__main__":
    test = DataBase('tables.db')
    print(test.getTables())
    print(test.getColumn('dept'))
    test.close()