import sqlite3

class FuncDep:
    def __init__(self, tableName, lhs, rhs, connection):
        self.tableName = tableName
        self.lhs = lhs
        self.rhs = rhs
        self.connection = connection

    def __str__(self):
        return self.tableName +" : ("+ self.lhs+") -> " + self.rhs

    def check(self):
        cursor = self.connection.execute("SELECT {},{} from {};".format(concat(self.lhs.split(',')),self.rhs,self.tableName))
        dico = {}
        for i in cursor:
            if (i[:len(i)-1] in dico.keys()) and (dico[i[:len(i)-1]] != i[len(i)-1]):
                return False
            dico[i[:len(i)-1]] = i[len(i)-1]
        
        return True
            


    

def concat(l):
    chain = ''
    for i in range(len(l)-1):
        chain+=l[i]
        chain+=','
    chain+=l[len(l)-1]
    return chain