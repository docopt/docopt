#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an interactive command application.

Usage:
    my_program tcp <host> <port> [--timeout=<seconds>]
    my_program serial <port> [--baud=<n>] [--timeout=<seconds>]
    my_program (-i | --interactive)
    my_program (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys, cmd
from docopt import docopt

class MyInteractive (cmd.Cmd):
    intro   = 'Welcome to my interactive program! (type help for a list of commands.)'
    prompt  = '(my_program) '
    file    = None
    
    def do_tcp(self, arg):
        """Usage: tcp <host> <port> [--timeout=<seconds>]"""
        
        doc = self.do_tcp.__doc__ 
        
        try:
            opt = docopt(doc,arg)
        except:
            print(doc)
            return
            
        print(opt)

    def do_serial(self, arg):
        """Usage: serial <port> [--baud=<n>] [--timeout=<seconds>]
Options:
    --baud=<n>  Baudrate [default: 9600]
        """

        doc = self.do_serial.__doc__

        try:
            opt = docopt(doc,arg)
        except:
            print(doc)
            return

        print(opt)
    
    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']: 
    MyInteractive().cmdloop()

print(opt)
