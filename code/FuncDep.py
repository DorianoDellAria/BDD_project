import sqlite3

class FuncDep:
    def __init__(self, tableName, lhs, rhs):
        self.tableName = tableName
        self.lhs = lhs
        self.rhs = rhs
        

    def __str__(self):
        return self.tableName +" : ("+ self.lhs+") -> " + self.rhs

    def check(self,other):
        cursor = other.db.execute("SELECT {},{} from {};".format(commaConcat(self.lhs.split(' ')),self.rhs,self.tableName))
        dico = {}
        for i in cursor:
            if (i[:len(i)-1] in dico.keys()) and (dico[i[:len(i)-1]] != i[len(i)-1]):
                return False
            dico[i[:len(i)-1]] = i[len(i)-1]
        
        return True
    
    def __eq__(self,other):
        if self.tableName==other.tableName and self.lhs==other.lhs and self.rhs==other.rhs:
            return True
        return False
            


    

def concat(l):
    chain = ''
    for i in range(len(l)-1):
        chain+=l[i]
        chain+=' '
    chain+=l[len(l)-1]
    return chain

def commaConcat(l):
    chain = ''
    for i in range(len(l)-1):
        chain+=l[i]
        chain+=','
    chain+=l[len(l)-1]
    return chain