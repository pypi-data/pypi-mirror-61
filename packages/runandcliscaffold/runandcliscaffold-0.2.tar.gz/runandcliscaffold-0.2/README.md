# runandcliscaffold
Lightweight library for use of defining functions and parameters that can be called from CLI or from other functions

Classes can now be defined in a simpler format that focus on business logic while enabling content for CLI running OR being called as a script

For example, a class definition:

    from runandcliscaffold import RunAndCliScaffold
    
    class fakeImplementation(RunAndCliScaffold):
        def __init__(self):
            super().__init__("TESTING")
    
        def hello(self, args):
            ret = f"{args.greeting}, {args.name}!"
            print(ret)
            return ret
    
        def goodbye(self, args):
            ret = f"{args.greeting}, {args.name}!"
            print(ret)
            return ret
    
        def _defineFunctionsWithArgs(self):
            return {self.hello: [{"short": "n", "long": "name", "default": "Tj", "type": str,
                                 "help": "test1: beginning of data collection time period"},
                                {"short": "g", "long": "greeting", "default": "Hello", "type": str, "required": False,
                                 "help": "greeting to use"}
                            ],
                    self.goodbye: [{"short": "n", "long": "name", "default": "Tj", "type": str,
                               "help": "test1: beginning of data collection time period"},
                              {"short": "g", "long": "greeting", "default": "Goodbye", "type": str, "required": False,
                               "help": "greeting to use"}
                              ],
            }


can be called through command line:
    
    python myscript.py hello -n Mark -g Wassup
and returns:
    
    Wassup, Mark!
    
the equivelant call from script:

    testclass = fakeImplementation()
    ret = testclass.run(['hello', '--g', 'Wassup', '--n', 'Mark'])
    
also returns the value:

    Wassup, Mark 

While enabling an app to be run out as CLI, this also has usage as a test mechanism or as a self contained unit for consumption of other scripts.