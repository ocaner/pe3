#!/usr/bin/env python3

from struct import unpack

class OpCodeCallBack(object):

    def opcode_error(self, addr, opcode, mne, error):
        pass

    def opcode_success(self, addr, opcode, mne):
        pass

class OpCodes(object):

    NOOP = 0x0

    addr = None

    opcode = None

    callback = None

    def error(self, addr, opcode, msg, error):
        if not self.callback:
            return
        self.callback.opcode_error(addr, opcode, msg, error)

    def notify(self, addr, opcode, msg):
        if not self.callback:
            return

        self.callback.opcode_success(addr, opcode, msg)

    def opcode_hook(self, opcode):
        pass

    def parse(self, addr, dword):
        print(f"{addr:08x} => {dword:08x}")
        self.addr = addr
        self.opcode = unpack("<I", dword)[0]
        print(f"> {addr:08x} ==> HEX: {self.opcode:08x} / {self.opcode:032b}")

        if OpCode.NOOP == self.opcode:
            print("=> NOOP")
            self.cb(addr, self.opcode, "NOOP")
            return

        self.opcode_hook()

        
