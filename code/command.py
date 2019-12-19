import cmd
import argparse

class command(cmd.Cmd):

    def __init__(self,data, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.data = data

        self.afd_parser = argparse.ArgumentParser(prog="add_fd")
        self.afd_parser.add_argument('table', help="table",nargs='?')
        self.afd_parser.add_argument('lhs',help="left arrow",nargs='?')
        self.afd_parser.add_argument('rhs',help="right arrow",nargs='?')

        self.column_parser = argparse.ArgumentParser(prog="column")
        self.column_parser.add_argument('table', help = 'name of the table')

        self.rm_parser = argparse.ArgumentParser(prog='rmfd')
        self.rm_parser.add_argument('fd',help='number of the fd',default=-1,type=int,nargs='?')

        self.closure_parser = argparse.ArgumentParser(prog="closure")
        self.closure_parser.add_argument('table', help='name of the table')
        self.closure_parser.add_argument('element',help='element')

        self.cons_parser=argparse.ArgumentParser(prog='cons')
        self.cons_parser.add_argument('table',help='name of the table')

        self.key_parser = argparse.ArgumentParser(prog='key')
        self.key_parser.add_argument('table', help='name of the table')

    intro = 'Bienvenue\n'
    prompt = 'sqlfat>'

    def do_EOF(self, line):
        self.data.close()
        return True

    def do_exit(self, line):
        self.data.close()
        return True

    def do_add_fd(self, line):
        try:
            if len(line) != 0:
                parsed = self.afd_parser.parse_args(line.split())
                self.data.addFuncDep(parsed.table,parsed.lhs, parsed.rhs)
            else:
                print(self.data.getTables())
                table = str(input('Enter the table : '))
                print(self.data.getColumn(table))
                lhs = str(input('lhs : '))
                print(self.data.getColumn(table))
                rhs = str(input('rhs :'))
                self.data.addFuncDep(table,lhs,rhs)
        except SystemExit:
            return
    
    def help_add_fd(self):
        self.afd_parser.print_help()

    def do_tables(self, line):
        print(self.data.getTables())
    
    def do_fd(self, line):
        print(self.data.getFD())

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
            print(self.data.closure(parsed.element,self.data.df,parsed.table))
        except SystemExit:
            return
    
    def do_cons(self,line):
        try:
            parsed = self.cons_parser.parse_args(line.split())
            self.data.cons(parsed.table)
        except SystemExit:
            return
    
    def do_key(self,line):
        try:
            parsed = self.key_parser.parse_args(line.split())
            print(self.data.key(parsed.table))
        except SystemExit:
            return



if __name__ == "__main__":
    command(None).cmdloop()