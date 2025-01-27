import cmd
import argparse
from FuncDep import concat

class command(cmd.Cmd):

    def __init__(self,data, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.data = data

        self.afd_parser = argparse.ArgumentParser(prog="addfd")
        self.afd_parser.add_argument('table', help="table",nargs='+')

        self.fd_parser = argparse.ArgumentParser(prog='fd')
        self.fd_parser.add_argument('table', help='name of the table', nargs='?')

        self.column_parser = argparse.ArgumentParser(prog="column")
        self.column_parser.add_argument('table', help = 'name of the table')

        self.rm_parser = argparse.ArgumentParser(prog='rmfd')
        self.rm_parser.add_argument('fd',help='number of the fd',default=-1,type=int,nargs='?')

        self.closure_parser = argparse.ArgumentParser(prog="closure")
        self.closure_parser.add_argument('table', help='name of the table')
        self.closure_parser.add_argument('element',help='element',nargs='+')

        self.cons_parser=argparse.ArgumentParser(prog='cons')
        self.cons_parser.add_argument('table',help='name of the table')

        self.key_parser = argparse.ArgumentParser(prog='key')
        self.key_parser.add_argument('table', help='name of the table')

        self.bcnf_parser = argparse.ArgumentParser(prog='bcnf')
        self.bcnf_parser.add_argument('table', help='name of the table')

        self.threenf_parser = argparse.ArgumentParser(prog='3nf')
        self.threenf_parser.add_argument('table', help='name of the table')

        self.decomp_parser = argparse.ArgumentParser(prog='decomposition')
        self.decomp_parser.add_argument('table', help='name of the table')
        self.decomp_parser.add_argument('db',help='name of the database',nargs='?',default='decomposition.db')

    intro = 'Bienvenue\n'
    prompt = '> '

    def do_EOF(self, line):
        self.data.close()
        return True

    def do_exit(self, line):
        self.data.close()
        return True

    def do_addfd(self, line):
        try:
            if len(line) != 0:
                parsed = self.afd_parser.parse_args(line.split())
                if len(parsed.table) >=3:
                    lhs = parsed.table[1:len(parsed.table)-1]
                    lhs = concat(lhs)
                    self.data.addFuncDep(parsed.table[0],lhs, parsed.table[-1])
                else:
                    print('argument missed')
            else:
                print(self.data.getTables())
                table = str(input('Enter the table : '))
                print(self.data.getColumn(table))
                lhs = str(input('lhs : '))
                print(self.data.getColumn(table))
                rhs = str(input('rhs : '))
                self.data.addFuncDep(table,lhs,rhs)
        except SystemExit:
            return
    

    def do_tables(self, line):
        print(self.data.getTables())

    
    def do_fd(self, line):
        try:
            parsed=self.fd_parser.parse_args(line.split())
            print(self.data.getFD(parsed.table))
        except SystemExit:
            return

    def do_column(self,line):
        try:
            parsed = self.column_parser.parse_args(line.split())
            print(self.data.getColumn(parsed.table))
        except SystemExit:
            return

    def do_rmfd(self, line):
        try:
            parsed = self.rm_parser.parse_args(line.split())
            self.data.removeFuncDep(parsed.fd)
        except SystemExit:
            return
    
    def do_check(self,line):
        self.data.checkFD()

    def do_closure(self,line):
        try:
            parsed= self.closure_parser.parse_args(line.split())
            element = concat(parsed.element)
            print(self.data.closure(element,self.data.df,parsed.table))
        except SystemExit:
            return
    
    def do_cons(self,line):
        try:
            parsed = self.cons_parser.parse_args(line.split())
            toDel = self.data.cons(parsed.table)
            for i in toDel:
                print(i)
            if len(toDel)!=0:
                answer = str(input('Do you want do delete ? (y/n) : '))
                if answer == 'y':
                    for i in toDel:
                        self.data.removeFuncDep(self.data.df.index(i))
        except SystemExit:
            return
    
    def do_key(self,line):
        try:
            parsed = self.key_parser.parse_args(line.split())
            print(self.data.sKey(parsed.table))
        except SystemExit:
            return
        
    def do_bcnf(self,line):
        try:
            parsed = self.bcnf_parser.parse_args(line.split())
            if self.data.checkBCNF(parsed.table):
                print('the table '+parsed.table+' is in BCNF')
            else:
                print('the table '+parsed.table+' isn\'t in BCNF')
        except SystemExit:
            return

    def do_3nf(self,line):
        try:
            parsed = self.threenf_parser.parse_args(line.split())
            if (self.data.check3NF(parsed.table)):
                print('the table '+parsed.table+' is in 3NF')
            else:
                print('the table '+parsed.table+' isn\'t in 3NF')
        except SystemExit:
            return
    
    def do_decompose(self,line):
        try:
            parsed= self.decomp_parser.parse_args(line.split())
            if not self.data.check3NF(parsed.table):
                self.data.decompose(parsed.table,parsed.db)
            else:
                print("this table is already in 3NF")
        except SystemExit:
            return



if __name__ == "__main__":
    command(None).cmdloop()