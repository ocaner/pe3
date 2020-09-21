#!/usr/bin/env python3

from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass, fields

GPR_NAMES = ("zero", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1",
             "t2", "t3", "t4", "t5", "t6", "t7", "s0", "s1", "s2", "s3", "s4",
             "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
             "pc", "hi", "lo", "hi1", "lo1", "sa")

GPR_DEFAULTS = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             # pc
             0xbfc00000, 
             0, 0, 0, 0, 0)


CPR_NAMES = ("idx", "rand", "elo0", "elo1", "ctx", "pm", "wire", "res0", "bva",
             "cnt", "ehi", "comp", "stat", "caus", "epc", "prid", "conf",
             "res1", "bpa", "dbg", "perf", "res2", "tlo", "thi", "eepc",
             "res3")

CPR_DEFAULTS = (
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 
             # PRId
             0x59, 
             0,
             0, 0, 
             # Debug
             0, 
             0, 0, 0, 0, 0, 0)

VPU_NAMES = ("vf00", "vf01", "vf02", "vf03", "vf04", "vf05", "vf06", "vf07",
             "vf08", "vf09", "vf10", "vf11", "vf12", "vf13", "vf14", "vf15",
             "vf16", "vf17", "vf18", "vf19", "vf20", "vf21", "vf22", "vf23",
             "vf24", "vf25", "vf26", "vf27", "vf28", "vf29", "vf30", "vf31",
             "vi00", "vi01", "vi02", "vi03", "vi04", "vi05", "vi06", "vi07",
             "vi08", "vi09", "vi10", "vi11", "vi12", "vi13", "vi14", "vi15",
             "acc", "q", "p")


#class Registers(NamedTuple):

    #def __init__(self, typeName, names, defaults=None):
    #    klazz = namedtuple(typeName, names, defaults=defaults)
    #    self.__obj__ = klazz()

    # def __getattr__(self, name):
    #     if name in self.__obj__._fields:
    #         return getattr(self.__obj__, name)

    #     return super().__getattr__(name)

    # def __setattr__(self, name, value):
    #     if name in self.__obj__._fields:
    #         setattr(self.__obj__, name, value)
        
    #     #setattr(self, name, value)
    #     super().__setattr__(name, value)

    # def name(self, register):
    #     return self._fields[register]

    # def __getitem__(self, register):
    #     return getattr(self, self._fields[register])
    
    # def __setitem__(self, register, value):
    #     setattr(self, self._fields[register], value)
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

    #def __init__(self):
    #    super().__init__("XGPR", GPR_NAMES, defaults=GPR_DEFAULTS)

#class CPR(Registers):

#    def __init__(self):
#        super().__init__("XCPR", CPR_NAMES, defaults=CPR_DEFAULTS)

#gpr = GPR()
#GPR = namedtuple('GPR', GPR_NAMES, defaults=GPR_DEFAULTS)
#CPR = namedtuple('CPR', CPR_NAMES, defaults=CPR_DEFAULTS)
#VPR = namedtuple('VPR', VPU_NAMES)

print(len(GPR_DEFAULTS))
print(*GPR_DEFAULTS)

gpr = GPR(*GPR_DEFAULTS)
#gpr.PC=0xbfc00000
#cpr = CPR()

gpr.PC += 4
gpr[32] += 4
print(f"GPR PC  : {gpr.PC:08x}")
print(dir(gpr))
print(fields(gpr)[32])

print(f"GPR[32] : {gpr[32]:08x}")
print(f"GPRN[32]: {fields(gpr)[32].name}")
print(f"len(GPR): {len(gpr)}")
#print(f"CPR PRId: {cpr.prid:08x}")
