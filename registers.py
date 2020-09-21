#!/usr/bin/env python3


#from collections import namedtuple
#from typing import NamedTuple
from dataclasses import dataclass, fields

PROCESSOR_ID = 0x59

BIOS_ADDR  = 0xbfc00000
BIOS_ADDR2 = 0x9fc00000
BIOS_ADDR3 = 0x1fc00000

GPR_DEFAULTS = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # pc
            BIOS_ADDR, 
            0, 0, 0, 0, 0)


CPR_DEFAULTS = (
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 
            # PRId
            PROCESSOR_ID, 
            0,
            0, 0, 
            # Debug
            0, 
            0, 0, 0, 0, 0, 0)

def name(registers, register):
    return fields(registers)[register].name

def createGPR():
    return GPR(*GPR_DEFAULTS)

def createCPR():
    return CPR(*CPR_DEFAULTS)

@dataclass
class CPR:
    Index: int
    Random: int
    EntryLo0: int
    EntryLo1: int
    Context: int
    PageMask: int
    Wired: int
    Reserved0: int
    BadVAddr: int
    Count: int
    EntryHi: int
    Compare: int
    Status: int
    Cause: int
    EPC: int
    PRId: int
    Config: int
    Reserved1: int
    BadPAddr: int
    Debug: int
    Perf: int
    Reserved2: int
    TagLo: int
    TagHi: int
    ErrorEPC: int
    Reserved3: int

    def __getitem__(self, register):
        return self.__getattribute__(fields(self)[register].name)

    def __setitem__(self, register, value):
        return self.__setattr__(fields(self)[register].name, value)

    def __len__(self):
        return len(fields(self))

@dataclass
class GPR:

    Zero: int
    AT: int 
    V0: int 
    V1: int
    A0: int
    A1: int
    A2: int
    A3: int
    T0: int
    T1: int
    T2: int

    T3: int
    T4: int
    T5: int
    T6: int
    T7: int
    S0: int
    S1: int
    S2: int
    S3: int
    S4: int
    S5: int
    S6: int 
    S7: int
    T8: int
    T9: int
    K0: int
    K1: int
    GP: int
    SP: int
    FP: int
    RA: int    
    PC: int
    Hi: int
    Lo: int
    Hi1: int
    Lo1: int
    SA: int

    def __getitem__(self, register):
        return self.__getattribute__(fields(self)[register].name)

    def __setitem__(self, register, value):
        return self.__setattr__(fields(self)[register].name, value)

    def __len__(self):
        return len(fields(self))

class VPU:
    REGISTER_NAMES = ("vf00", "vf01", "vf02", "vf03", "vf04", "vf05", "vf06", "vf07",
        "vf08", "vf09",
        "vf10",
        "vf11",
        "vf12",
        "vf13",
        "vf14",
        "vf15",
        "vf16",
        "vf17",
        "vf18",
        "vf19",
        "vf20",
        "vf21",
        "vf22",
        "vf23",
        "vf24",
        "vf25",
        "vf26",
        "vf27",
        "vf28",
        "vf29",
        "vf30",
        "vf31",
        "vi00",
        "vi01",
        "vi02",
        "vi03",
        "vi04",
        "vi05",
        "vi06",
        "vi07",
        "vi08",
        "vi09",
        "vi10",
        "vi11",
        "vi12",
        "vi13",
        "vi14",
        "vi15",
        "acc",
        "q", "p"
    )

    def __init__(self):
        self.registers = Registers(VPU.REGISTER_NAMES, typed=True)
