import cmd
import argparse

class command(cmd.Cmd):

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)

        self.foo_parser = argparse.ArgumentParser(prog="foo")
        self.foo_parser.add_argument('--test', help="test help")

    intro = 'Bienvenue\n'
    prompt = 'sqlfat>'

    def do_EOF(self, line):
        return True

    def do_foo(self, line):
        try:
            parsed = self.foo_parser.parse_args(line.split())
        except SystemExit:
            return
        print('bar', parsed.test if parsed.test!=None else '')

    def help_foo(self):
        self.foo_parser.print_help()

    def do_exit(self, line):
        return True




if __name__ == "__main__":
    command().cmdloop()