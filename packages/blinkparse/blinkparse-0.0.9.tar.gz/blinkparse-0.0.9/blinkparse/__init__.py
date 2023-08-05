# Author: Nathan Merrill (@nathansmerrill)

import sys

from blinkparse.arguments import Arguments
from blinkparse.argument import Argument
from blinkparse.command import Command
from blinkparse.commandArgument import CommandArgument

def displayHelpPage(args, commands, description, commandRequired):
    if description != '':
        print(description.strip())

    if len(commands) != 0:
        if commandRequired:
            print('Commands - Required')
        else:
            print('Commands')

        for command in commands:
            print('    ', command.name)
            for commandArg in command.args:
                print(f'        {commandArg.name}: {commandArg.options if commandArg.options is not None else "anything"}{" - Required" if commandArg.required else ""}')

    print('Arguments')
    for arg in args:
        argText = ''
        if arg.takesValue:
            argText += f'--{arg.name}=myValue'
            if arg.shortName is not None:
                argText += f', -{arg.shortName} myValue'
        else:
            argText += f'--{arg.name}'
            if arg.shortName is not None:
                argText += f', -{arg.shortName}'
        print(f'    {argText}')
        print(f'        {arg.description}')
        if arg.required:
            print('        Required')
    sys.exit()

def parse(args=[], commands=[], description='', commandRequired=False, inputArgs=None):
    args.append(Argument('help', 'h', description='Show this help page'))
    if inputArgs is None:
        inputArgs = sys.argv[1:]

    # Help page - this isn't a normal argument because it needs to be parsed before the others
    if '-h' in inputArgs or '--help' in inputArgs:
        displayHelpPage(args, commands, description, commandRequired)

    if len(commands) != 0:
        try:
            inputCommand = inputArgs[0]
        except IndexError:
            raise ValueError(f'This program requires a command. The options are {list(loopCommand.name for loopCommand in commands)}')
        for command in commands:
            commandArgs = command.check(inputCommand, inputArgs)
            if commandArgs is not None:
                break
            else:
                command = None
    else:
        command = None
        commandArgs = None

    if command is None and commandRequired:
        raise ValueError(f'This program requires a command. The options are {list(loopCommand.name for loopCommand in commands)}')

    outputArgs = {}
    for arg in args:
        outputArgs.update(arg.check(inputArgs))

    return Arguments(outputArgs, inputArgs, command.name if command is not None else None, commandArgs)
