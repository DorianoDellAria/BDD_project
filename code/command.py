import cmd
import argparse

class command(cmd.Cmd):

    def __init__(self,data, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.data = data

        self.afd_parser = argparse.ArgumentParser(prog="add")
        self.afd_parser.add_argument('table', help="table")
        self.afd_parser.add_argument('lhs',help="left arrow")
        self.afd_parser.add_argument('rhs',help="right arrow")

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
            parsed = self.afd_parser.parse_args(line.split())
            self.data.addFuncDep(parsed.table,parsed.lhs, parsed.rhs)
        except SystemExit:
            return
    
    def help_add_fd(self):
        self.afd_parser.print_help()

    def do_tables(self, line):
        print(self.data.printTables())



if __name__ == "__main__":
    command(None).cmdloop()