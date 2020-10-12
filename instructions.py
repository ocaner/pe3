#!/usr/bin/env python3

from yaml import load, SafeLoader
from jinja2 import Environment, FileSystemLoader, select_autoescape

FORMAT = "F"
MATCH = "M"
PATTERN = "P"
SHIFT_LEFT = "SHL"
SHIFT_RIGHT = "SHR"

class Instruction:

    @classmethod
    def create(cls, name, options):
        pattern = None
        match = None
        fmt = ""

        args = []

        for k, v in options.items():
            if PATTERN == k:
                pattern = v
            elif MATCH == k:
                match = v
            elif FORMAT == k:
                fmt = v
            else:
                args.append( Arg.create(k, v) )

        obj = cls(name, pattern, match, fmt=fmt)
        obj.args = args
        return obj

    def __init__(self, name, pattern, match, fmt=""):
        self.name = name
        self.pattern = pattern
        self.match = match
        self.format = fmt
        self.args = None

class Arg:

    @classmethod
    def create(cls, name, options):
        pattern = None
        shl = None
        shr = None

        for k, v in options.items():
            if PATTERN == k:
                pattern = v
            elif SHIFT_LEFT == k:
                shl = v
            elif SHIFT_RIGHT == k:
                shr = v
        
        obj = cls(name, pattern)
        
        if shl:
            obj.shl = shl
        elif shr:
            obj.shr = shr
        
        return obj
    
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
        self.shl = 0
        self.shr = 0
    
    

instructions = None

with open("instructions.yml", "r") as fi:
    instructions = load(fi, Loader=SafeLoader)

#print(instructions)

instrs = []

for instruction, options in instructions.items():
    
    instr = Instruction.create(instruction, options)

    instrs.append(instr)

    #print(f"{instr.name.upper()} => {instr}")

def pbin(value, size=32):
    fmt = "{{0:0{0}b}}".format(size)
    return fmt.format(value)

def wbin(value):
    return pbin(value, size=16)

def dwbin(value):
    return pbin(value, size=32)

def qwbin(value):
    return pbin(value, size=64)

env = Environment(
    loader=FileSystemLoader('./')
)
env.filters["hex"] = hex
env.filters["bin"] = pbin
env.filters["wbin"] = wbin
env.filters["dwbin"] = dwbin
env.filters["qwbin"] = qwbin

template = env.get_template("opcodes.py.j2")
print(template.render(instructions=instrs))