#!/usr/bin/env python3

from bios import BIOS
from cpu import R5900

#BIOS_PATH = "bios/scph39001.bin"
#BIOS_PATH = "bios/scph10000.bin"
BIOS_PATH = "bios/SCPH-70004_BIOS_V12_PAL_200.BIN"

class PE3:
    def __init__(self, bios=BIOS_PATH):
        self.bios_path = bios
        self.bios = BIOS(self.bios_path)
        self.cpu = R5900(self.bios)

    def run(self):
        self.cpu.run()

if __name__ == "__main__":
    pe3 = PE3()
    pe3.run()