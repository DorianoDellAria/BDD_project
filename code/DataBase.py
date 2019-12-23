import sqlite3
import FuncDep
from copy import deepcopy
from random import shuffle

class DataBase:
    def __init__(self, name):
        self.name = name
        self.db = sqlite3.connect(name)
        self.df = []
        if 'FuncDep' in self.getTables():
            cursor = self.db.execute('SELECT * FROM FuncDep;')
            for t in cursor:
                self.df += [FuncDep.FuncDep(t[0],t[1],t[2]),]

    """imprime les tables de la database"""
    def getTables(self)->list:
        cursor = self.db.execute("SELECT * FROM sqlite_master WHERE type='table'")
        chain = []
        for i in cursor:
            chain += [i[2],]
        return chain

    """imprime les colonnes d'une table"""
    def getColumn(self, table):
        if table not in self.getTables():
            return "this table doesn't exist"
        cursor = self.db.execute("SELECT * FROM " + table)
        return list(map(lambda x: x[0],cursor.description))

    """ferme la DB"""
    def close(self):
        self.db.close()
        print("\ndata base closed")
        
    """ajout de dépendances fonctionnelles"""
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
        newLHS=lhs.split()[0]
        for i in lhs.split(' '):
            if i not in self.getColumn(tableName):
                print("lhs : this column doesn't exist")
                return
            if i not in newLHS:
                newLHS+= ' '+i
        
        """condition d'existance de la droite"""
        if rhs not in self.getColumn(tableName):
            print("rhs : this column doesn't exist")
            return
        
        tmp = 'INSERT INTO FuncDep VALUES (?,?,?);'
        self.db.execute(tmp,(tableName,newLHS,rhs))
        self.db.commit()
        self.df += [FuncDep.FuncDep(tableName,newLHS,rhs),]
    
    """imprime les DF d'une database"""
    def getFD(self, table=None)->str:
        chain =''
        for i in range(len(self.df)):
            if table==None or table==self.df[i].tableName:
                chain+=str(i) + " : "+ str(self.df[i])
                chain+='\n'
        return chain

    """supprime les DF"""
    def removeFuncDep(self,number)->None:
        if number == -1:
            print(self.getFD())
            number = int(input("which one do you want to remove ? : "))

        if len(self.df) == 0 or number < 0 or number >= len(self.df):
            print("this FD doesn't exist")
            return
        
        self.db.execute("DELETE FROM FuncDep where table_name = ? and lhs = ? and rhs = ?;",(self.df[number].tableName,self.df[number].lhs,self.df[number].rhs))
        self.db.commit()
        self.df.pop(number)
    
    """vérifie si les DF sont respectée"""
    def checkFD(self)->None:
        for i in self.df:
            print(i, " : ", i.check(self))

    """fermeture d'un ensemble d'attribut où X est l'ensemble d'attribut,
    F est la liste des DF et table est le nom de la table"""
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


    """affiche les DF qui sont conséquence des autres.
    table est le nom de la table à analyser"""
    def cons(self,table)->list:
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
                    # print(tmp[i])
                    res += [tmp.pop(i),]
                    b=True
                    break
        return res

    """envoie l'ensemble des superClés dans la méthode key()"""        
    def sKey(self, table)->list:
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
            return [obvious]
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

    """à partir d'un ensemble de superClé(sKey), calcule les clé minimales
    chain est l'ensemble d'attributs nécessaire pour former une clé"""
    def key(self,sKey:list,chain:str)->list:
        for i in range(len(sKey)):
            sKey[i] = sKey[i].replace(chain,'')
        result = deepcopy(sKey)
        for _ in range(len(sKey)):
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
    
    """vérifie qu'une table est en BCNF"""
    def checkBCNF(self, table:str)->bool:
        for i in self.df:
            if i.tableName==table and not include(self.getColumn(table),self.closure(i.lhs,self.df,table)):
                return False
        return True
    
    """vérfie qu'une table est en 3NF"""
    def check3NF(self,table:str)->bool:
        if self.checkBCNF(table):
            return True
        else:
            keys = self.sKey(table) 
            for i in self.df:
                if i.tableName==table and not include(self.getColumn(table),self.closure(i.lhs,self.df,table)) and (not includeInKey(i.rhs,keys)):
                    return False
            return True


    """decompose une table en 3NF
    table est le nom de la table
    fileName est le nom de la nouvelle Database"""
    def decompose(self,table:str,fileName:str):
        decomp = DataBase(fileName)

        '''deleting useless df'''
        copy = deepcopy(self.df)
        toDel = self.cons(table)
        if len(toDel)!=0:
            for i in toDel:
                copy.pop(copy.index(i))

        '''filter the fd'''
        fd = []
        for i in copy:
            if i.tableName == table:
                fd+=[i,]
        
        '''reseting database'''
        dtable=decomp.getTables()
        if len(dtable)!=0:
            for i in range(len(dtable)):
                decomp.db.execute("DROP TABLE {};".format(dtable[i]))
        
        '''creating tables'''
        decomp.db.execute("ATTACH DATABASE '{}' AS tmp;".format(self.name))
        typ=getType(self.db,table)
        for i in range(len(fd)):
            arr = fd[i].lhs.split()
            arr += [fd[i].rhs,]
            values = ''
            for j in range(len(arr)-1):
                values += arr[j]+' '+typ[arr[j]]+','
            values += arr[-1] + ' ' + typ[arr[-1]] 
            # print(values)
            decomp.db.execute("CREATE TABLE {} ({})".format(chr(i+65),values))
            decomp.addFuncDep(chr(i+65),FuncDep.concat(arr[0:len(arr)-1]),arr[-1])
            decomp.db.execute("INSERT INTO {} SELECT {} FROM tmp.{};".format(chr(i+65),FuncDep.commaConcat(arr),table))
            decomp.db.commit()
        

        keys = self.sKey(table)
        tmp = decomp.getTables()
        for i in range(len(keys)):
            test=True
            for j in range(len(tmp)):
                col = decomp.getColumn(tmp[i])
                if include(keys[i].split(),col):
                    test=False
                    break
            if test:
                values=''
                key = keys[i].split(' ')
                for j in range(len(key)-1):
                    values += key[j]+' '+typ[key[j]]+','
                values += key[-1]+' '+typ[key[-1]]
                decomp.db.execute("CREATE TABLE {} ({});".format('K'+chr(i+65),values))
                decomp.db.execute("INSERT INTO {} SELECT {} FROM tmp.{};".format('K'+chr(i+65),FuncDep.commaConcat(keys[i].split()),table))

        decomp.db.commit()
        decomp.db.execute("DETACH DATABASE 'tmp';")
        decomp.close()
    


"""retourne un dictionaire contenant le nom d'une colonne d'une table et son type"""
def getType(db:sqlite3.Connection,table:str)->dict:
    cursor = db.execute("PRAGMA table_info({})".format(table))
    res = {}
    for i in cursor:
        res[i[1]]=i[2]
    return res
        


"""vérifie si un élément est dans une clé"""
def includeInKey(rhs:str,keys:list)->bool:
    for i in keys:
        if rhs in i.split():
            return True
    return False

"""inclusion mathémathique. Se lit A est inclu à B"""
def include(a:list,b:list)->bool:
    for i in a:
        if i not in b:
            return False
    return True

"""retourne toutes les combinaison possible d'une liste.
Le code à été trouvé sur https://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n""" 
def choose_iter(elements, length):
    for i in range(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i+1:len(elements)], length-1):
                yield (elements[i],) + next

"""mets le résultat de choose_iter sous une autre forme"""
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
            
