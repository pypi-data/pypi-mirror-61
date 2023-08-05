# BlinkParse
A python library for parsing command line arguments
## Installation
`pip install --user blinkparse`
## Usage
#### `parse(args=[], commands=[], description='', commandRequired=False, inputArgs=None)`  
- Returns a `blinkparse.Arguments` object
- `args` is a list of `blinkparse.Argument` objects
- `commands` is a list of `blinkparse.Command` objects
- `description` is a description to show at the top of the help page  
- `commandRequired` is whether the program requires a command to be passed in
- `inputArgs` is an array of the arguments to parse. This defaults to `sys.argv[1:]`
#### `Argument(self, name, shortName=None, takesValue=False, required=False, description=None)`  
- `name` is the argument name used in the long syntax (`--myArg`, `--myArg=myValue`)
- `shortName` is the argument name used in the long syntax (`-a`, `-a myValue`)
- `takesValue` is whether the argument takes a input (see above)
- `required` makes the blinkparse raise an error if the argument isn't passed in
- `description` is a description to show in the help page  
#### `Command(self, name, args=[], aliases=[])`  
- Usage
    - `Command('hello', [CommandArgument('person'), CommandArgument('gender', required=False, options=['male', 'female', 'other])], 'h')`
    - `$ python3 example.py hello jered`
    - `$ python3 example.py hello joe male`
- `name` is the name of the command
- `args` is a list of `blinkparse.CommandArgument` objects that the command takes
- `CommandArgument(self, name, options=None, required=True)`
    - `name` is the name of the command argument
    - `options` is a list of allowed options for the argument (defaults to everything)
    - `required` makes blinkparse raise an error if the command argument isn't passed in
- `aliases` is a list of other names for the command
## Full example
```python
from blinkparse import *

args = parse(
    args=[
        Argument('save', 's', description='Save the program output'),
    ],
    commands=[
        Command('hello', [
            CommandArgument('person'),
            CommandArgument('gender', required=False, options=['male', 'female', 'other'])
        ]),
        Command('bye', [
            CommandArgument('person')
        ])
    ],
    description='''
hello.py
A simple demo of blinkparse
    ''',
    commandRequired=True
)

if args.command == 'hello':
    output = 'Hello ' + args.commandArgs['person']
    if 'gender' in args.commandArgs:
        output += ', you are ' + args.commandArgs['gender']
else:
    output = 'Bye ' + args.commandArgs['person']

if 'save' in args.args:
    with open('hello.txt', 'w') as outputFile:
        outputFile.write(output)
else:
    print(output)
```