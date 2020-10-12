#!/usr/bin/env python3

from collections import namedtuple
from struct import calcsize, unpack, pack
from yaml import load, SafeLoader
from math import log
from io import BytesIO

from registers import BIOS_ADDR, BIOS_ADDR2, BIOS_ADDR3, createGPR, createCPR, name
from R5900Gen import R5900Gen
#PRId = 15
#CPRId = 0x59

#PC = 32

MiB = 1024**2
KERNEL_SIZE = 1 * MiB
RAM_SIZE = 32 * MiB
REMAIN_RAM_SIZE = RAM_SIZE - KERNEL_SIZE
#BIOS_ADDR = 0xbfc00000

MEMORY_MAP=(
    (0,  0, KERNEL_SIZE, "Kernel"),
    (KERNEL_SIZE, KERNEL_SIZE, REMAIN_RAM_SIZE, "Main RAM"),
    (0x20000000, 0, RAM_SIZE, "Main RAM, uncached"),
    (0x30100000, KERNEL_SIZE, REMAIN_RAM_SIZE, "Main RAM, uncached and accelerated"),
    (0x10000000, 0x10000000, 65535, "I/O registers"),
    (0x11000000, 0x11000000, 4096, "VU0 code memory"),
    (0x11004000, 0x11004000, 4096, "VU0 data memory"),
    (0x11008000, 0x11008000, 16384, "VU1 code memory"),
    (0x1100C000, 0x1100C000, 16384, "VU1 data memory"),
    (0x12000000, 0x12000000, 8192, "GS privileged registers"),
    (0x1C000000, 0x1C000000, 2 * MiB, "IOP RAM"),
    (0x1FC00000, 0x1FC00000, 4 * MiB, "BIOS, uncached (rom0)"),
    (0x9FC00000, 0x1FC00000, 4 * MiB, "BIOS, cached (rom09)"),
    (0xBFC00000, 0x1FC00000, 4 * MiB, "BIOS, uncached (rom0b)"),
    (0x70000000, None,  16384, "Scratchpad RAM (only accessible via virtual addressing"),
)


class R5900(R5900Gen):

    def __init__(self, bios):
        self.exec = False
        self.callback = None

        # ROM
        self.bios = bios

        print(f"Using BIOS {self.bios.version_str} {self.bios.date} {self.bios.zone}")
        print(f"checksum BIOS = {self.bios.checksum():08x}")

        # RAM
        self.ram = bytearray([0] * RAM_SIZE) #BytesIO(bytes(R5900.RAM_SIZE))
        #self.bram = self.ram.getbuffer()

        # copy kernel to ram
        #self.bios.

        # HW
        #self.vu0 = VPU()
        #self.vu1 = VPU()
        self.GPR = createGPR() #Registers(R5900.GPR_NAMES)
        self.CPR = createCPR() #Registers(R5900.CPR_NAMES)

        self.initRAM()

        # init registers
        #self.GPR.set(R5900.PC, R5900.BIOS)
        #self.CPR.set(R5900.PRId, R5900.CPRId)
        

        #self.registers.len += vregs.len
        #self.registers.names += vregs.names
        #self.registers.regs += vregs.regs

        #print(f"YY {self.registers.names.index('pc')}")
        #with open("instructions.yml", "r") as fi:
        #  self.instr = load(fi, Loader=SafeLoader)

    def initRAM(self):
        # initialize RAM from ROM
        kernel, content = self.bios.get_file("KERNEL")

        if kernel:
            print(f"KERNEL ==> {kernel.file_size:08x} {kernel.offset:08x} {kernel}")
            #print(f"{content}")

            #for addr in range(kernel.file_size):
            self.write_buf(0x0, content)

        else:
            raise Exception("KERNEL not found")

    def cb(self, addr, op, mn, error=False):
        if self.callback:
            self.callback.callback(addr, op, mn, error=error)

    def args(self, meta, value):
        args = {}

        for k, m in meta.items():
            if k in ('F', 'M', 'P'):
                continue
            #p2 = log(p, 2).is_integer()
            args[k] = value & m['P']

            if "SHL" in m:
                args[k] = args[k] << m['SHL']
            elif "SHR" in m:
                args[k] = args[k] >> m['SHR']

            print(f"{k} ==> {args[k]}")

        Args = namedtuple('Args', args.keys(), defaults=args.values())
        a = Args()

        return a

    def read_qword(self, addr):
        virtual = False
        kuseg = False
        kseg0 = False
        kseg1 = False

        if addr >= 0x20000000:
            virtual = True

        if addr <= 0x7FFFFFFF:
            kuseg = True
        elif addr >= 0x80000000 and addr <=0x9FFFFFFF:
            kseg0 = True
        elif addr >= 0xA0000000 and addr <= 0xBFFFFFFF:
            kseg1 = True
        
        target = "N/A"

        for vaddr, paddr, size, descr in MEMORY_MAP:
            if virtual:
                if addr >= vaddr and addr < vaddr + size:
                    target = descr
                    break
            else:
                if paddr is None:
                    print("ONLY VIRTUAL")
                elif addr >= paddr and addr < paddr + size:
                    target = descr

        print(f"=================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f"RAM read {addr:08x} ==> {target} VIRT: {virtual} KUSEG: {kuseg} KSEG0: {kseg0} KSEG1: {kseg1}")

        if addr >= BIOS_ADDR and addr <= BIOS_ADDR + self.bios.size:
            return self.bios.read_qword(addr - BIOS_ADDR)
        elif addr >= BIOS_ADDR2 and addr <= BIOS_ADDR2 + self.bios.size:
            return self.bios.read_qword(addr - BIOS_ADDR2)
        elif addr >= BIOS_ADDR2 and addr <= BIOS_ADDR3 + self.bios.size:
            return self.bios.read_qword(addr - BIOS_ADDR3)
        
        #if addr >= 0 and addr < KERNEL_SIZE:
        #    self.bios.files

        res = self.ram[addr:addr+4]

        print(f"{addr:08x} - {addr + 4:08x} ==> {res}")

        if res == b'':
            self.ram[addr:addr+4] = [0, 0, 0, 0]
            res = self.ram[addr:addr+4]

        return res

    def write_buf(self, addr, buf):
        print(f"> WRITE BUF {addr:08x} => {len(buf):08x}")

        self.ram[addr:addr + len(buf)] = buf

    def write_word(self, addr, word):
        print(f"> WRITE WORD {addr:08x} => {word:04x}")
        #buf = bytearray((word & 0xFF00 >> 8, word & 0x00FF))
        #print(f"> {self.bram[addr:addr+2]} <== {buf}")

        self.ram[addr:addr+2] = [word & 0xFF00 >> 8, word & 0x00FF]
        #self.ram.seek(addr)
        #self.ram.write(bytes([word & 0xFF00 >> 8, word & 0x00FF]))

    def cycle(self, addr):
        w = self.read_qword(addr)

        self.parse(addr, w)

        return 

        print(f"{addr:08x} => {w}")
        c = unpack("<I", w)[0]
        print(f"> {addr:08x} ==> HEX: {c:08x} / {c:032b}")

        if c == 0x0:
            print("=> NOOP")
            self.cb(addr, c, "NOOP")
        elif c == 0x27bdffa0:
            print("=> UNKNOWN OP CODE {c:08x}, skipping")
            self.cb(addr, c, "UNKNOWN OP CODE")
        else:          
            found = False
            for k, v in self.instr.items():
                x = c & v['P']
                if v['M'] == x:
                    found = True
                    if k == "lui":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            immediate=args.immediate
                        )

                        print(f"=> {k.upper()} {oa}")
                        #self.GPR.set(args.rt, args.immediate & 0xFFFF0000)
                        self.GPR[args.rt] = args.immediate & 0xFFFF0000
                        #print(f"K0: {self.k0} ")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        break
                    elif k == "tlbwi":
                        args = self.args(v, c)
                        oa = v['F'].format()
                        print(f"=> {k.upper()} {oa}")

                        print(f"Index   : {self.CPR.Index:08x}")
                        print(f"PageMask: {self.CPR.PageMask:08x}")
                        print(f"EntryHi : {self.CPR.PageMask:08x}")
                        print(f"EntryLo0 : {self.CPR.PageMask:08x}")
                        print(f"EntryLo1 : {self.CPR.PageMask:08x}")

                        
                        #self.GPR.set(args.rt, args.immediate & 0xFFFF0000)
                        #print(f"K0: {self.k0} ")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        break
                    elif k == "li":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            val=args.val
                        )
                        print(f"=> {k.upper()} {oa}")
                        #self.GPR.set(args.rt, args.val)
                        #R5900.set_reg(self.GPR, args.rt, args.val)
                        self.GPR[args.rt] = args.val
                        #print(f"K0: {self.k0} ")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        break
                    elif k == "jr":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rs=name(self.GPR, args.rs)
                        )
                        print(f"=> {k.upper()} {oa}")

                        self.GPR.PC = self.GPR[args.rs]
                        
                        #self.GPR.set(R5900.PC, self.GPR.get(args.rs))
                        #self.GPR.PC = self.GPR[args.rs]
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        return -1
                    elif k == "jal":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            instr_index=args.instr_index
                        )
                        print(f"=> {k.upper()} {oa}")

                        #self.GPR.PC = self.GPR[args.rs]
                        #self.GPR.RA = self.GPR.PC + 8
                        #self.GPR.PC = ( self.GPR.PC + 4 & 0xF0000000 ) | args.instr_index
                        self.GPR.RA = self.GPR.PC + 12
                        self.GPR.PC = ( self.GPR.PC + 8 & 0xF0000000 ) | args.instr_index
                        
                        #self.GPR.set(R5900.PC, self.GPR.get(args.rs))
                        #self.GPR.PC = self.GPR[args.rs]
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        return -1
                    elif k == "jalr":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rs=name(self.GPR, args.rs),
                            rd=name(self.GPR, args.rd)
                        )
                        print(f"=> {k.upper()} {oa}")
                        #self.GPR.set(R5900.PC, self.GPR.get(args.rs))
                        t = self.GPR[args.rs]
                        #self.GPR[args.rd] = self.GPR.PC + 8
                        self.GPR[args.rd] = self.GPR.PC + 12
                        self.GPR.PC = t
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        return -1
                    elif k == "sync":
                        args = self.args(v, c)
                        oa = v['F'].format(stype=args.stype)
                        print(f"=> {k.upper()} {oa}")
                        # TODO implement SYNC                        
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        break
                    elif k == "ori":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            rs=name(self.GPR, args.rs), 
                            immediate=args.immediate
                        )
                        print(f"=> {k.upper()} {oa}")
                        self.GPR[args.rt] = self.GPR[args.rs] | args.immediate
                        #print(f"K0: {self.k0} ")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        print(f"{self.GPR}")
                        break
                    elif k == "bne":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            rs=name(self.GPR, args.rs), 
                            offset=args.offset
                        )
                        print(f"=> {k.upper()} {oa}")
                        print(f">> {args}")

                        self.cb(addr, c, f"{k.upper()} {oa}")

                        if self.GPR[args.rt] != self.GPR[args.rs]:
                            offset = args.offset << 2
                            print(f"JMP +{offset}")
                            self.GPR.PC = self.GPR.PC + 4 + offset
                            return -1                         
                        break
                    elif k == "sw":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            base=args.base, 
                            offset=args.offset
                        )
                        print(f"=> {k.upper()} {oa}")
                        print(f">> {args}")

                        write_addr = self.GPR[args.base] + args.offset

                        self.write_word(write_addr, self.GPR[args.rt] & 0xFFFF0000 )
                        self.write_word(write_addr + 2, self.GPR[args.rt] & 0x0000FFFF )

                        self.cb(addr, c, f"{k.upper()} {oa}")
                        break
                    elif k == "sd":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            base=args.base, 
                            offset=args.offset
                        )
                        print(f"=> {k.upper()} {oa}")
                        print(f">> {args}")

                        write_addr = self.GPR[args.base] + args.offset

                        self.write_word(write_addr, self.GPR[args.rt] & 0x0000FFFF )

                        self.cb(addr, c, f"{k.upper()} {oa}")
                        break
                    elif k == "mfc0":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt),
                            rd=name(self.CPR, args.rd)
                        )
                        print(f"=> {k.upper()} {oa}")
                        print(f">> {args}")
                        self.GPR[args.rt] = self.CPR[args.rd]
                        print(f"{self.GPR}")
                        print(f"{self.CPR}")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        break
                    elif k == "mtc0":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            rd=name(self.CPR, args.rd)
                        )
                        print(f"=> {k.upper()} {oa}")
                        print(f">> {args}")
                        self.CPR[args.rd] = self.GPR[args.rt]
                        print(f"{self.GPR}")
                        print(f"{self.CPR}")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        break
                    elif k == "slti":
                        args = self.args(v, c)
                        oa = v['F'].format(
                            rt=name(self.GPR, args.rt), 
                            rs=name(self.GPR, args.rs), 
                            immediate=args.immediate
                        )
                        print(f"=> {k.upper()} {oa}")
                        self.GPR[args.rt] = 1 if self.GPR[args.rs] < args.immediate else 0
                        print(f"{self.GPR}")
                        self.cb(addr, c, f"{k.upper()} {oa}")
                        break
            if not found:
                self.cb(addr, c, "N/A", error=True)
                print(f"XXX {addr:08x} {c:08x} UNHANDLED OP CODE XXX")
                big = pack(">I", c)
                little = pack("<I", c)
                print(f"{big} {little}")
        return 4

    def inc_pc(self):
        self.GPR.PC += 4

    def run(self):
        self.exec = True
        self.GPR.set(R5900.PC, 0)

        while self.exec:
            addr = self.GPR.get(R5900.PC)
            #size = self.cycle(addr)

            #if size != -1:
            #    self.GPR.set(R5900.PC, addr + size)

            #if self.GPR.get(R5900.PC) >= 256:
            #    self.exec = False

    def instr_tlbwi( self, fmt ):
        mne = fmt.format()
        print(f"=> {mne}")

        print(f"Index   : {self.CPR.Index:08x}")
        print(f"PageMask: {self.CPR.PageMask:08x}")
        print(f"EntryHi : {self.CPR.PageMask:08x}")
        print(f"EntryLo0 : {self.CPR.PageMask:08x}")
        print(f"EntryLo1 : {self.CPR.PageMask:08x}")

        
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_bne( self, fmt,  rs ,   rt ,   offset   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rs=name(self.GPR, rs), 
            offset=offset
        )

        self.notify(self.addr, self.opcode, f"{mne}")

        if self.GPR[rt] != self.GPR[rs]:
            offset = offset << 2
            print(f"JMP +{offset}")
            self.GPR.PC = self.GPR.PC + 4 + offset
        else:
            self.inc_pc()

    def instr_sd( self, fmt,  base ,   rt ,   offset   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            base=base, 
            offset=offset
        )

        write_addr = self.GPR[base] + offset

        self.write_word(write_addr, self.GPR[rt] & 0x0000FFFF )

        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()


    def instr_lw( self, fmt,  base ,   rt ,   offset   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            base=base, 
            offset=offset
        )

        read_addr = self.GPR[base] + offset

        #t = self.read_word(read_addr)  << 16
        #t = t | self.read_word(write_addr + 2)

        # XXX TLB

        self.GPR[rt] = unpack("<I", self.read_qword(read_addr))[0]

        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()


    def instr_sw( self, fmt,  base ,   rt ,   offset   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            base=base, 
            offset=offset
        )

        write_addr = self.GPR[base] + offset

        self.write_word(write_addr, self.GPR[rt] & 0xFFFF0000 )
        self.write_word(write_addr + 2, self.GPR[rt] & 0x0000FFFF )

        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_jal( self, fmt,  instr_index   ):
        mne = fmt.format(
            instr_index=instr_index
        )

        #self.GPR.PC = self.GPR[rs]
        #self.GPR.RA = self.GPR.PC + 8
        #self.GPR.PC = ( self.GPR.PC + 4 & 0xF0000000 ) | instr_index
        self.GPR.RA = self.GPR.PC + 12
        self.GPR.PC = ( self.GPR.PC + 8 & 0xF0000000 ) | instr_index
        
        self.notify(self.addr, self.opcode, f"{mne}")

    def instr_jr( self, fmt,  rs   ):
        mne = fmt.format(
            rs=name(self.GPR, rs)
        )

        self.GPR.PC = self.GPR[rs]
        
        self.notify(self.addr, self.opcode, f"{mne}")

    def instr_jalr( self, fmt,  rs ,   rd   ):
        mne = fmt.format(
            rs=name(self.GPR, rs),
            rd=name(self.GPR, rd)
        )
        #self.GPR.set(R5900.PC, self.GPR.get(rs))
        t = self.GPR[rs]
        #self.GPR[rd] = self.GPR.PC + 8
        self.GPR[rd] = self.GPR.PC + 12
        self.GPR.PC = t
        self.notify(self.addr, self.opcode, f"{mne}")

    def instr_sync( self, fmt,  stype   ):
        mne = fmt.format(stype=stype)
        # TODO implement SYNC                        
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_li( self, fmt,  rt ,   val   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            val=val
        )
        self.GPR[rt] = val
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_lui( self, fmt,  rt ,   immediate   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            immediate=immediate
        )

        self.GPR[rt] = immediate & 0xFFFF0000
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_mfc0( self, fmt,  rt ,   rd   ):
        mne = fmt.format(
            rt=name(self.GPR, rt),
            rd=name(self.CPR, rd)
        )
        self.GPR[rt] = self.CPR[rd]
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_mfc1( self, fmt,  rt ,   fs   ):
        
        pass

    def instr_mtc0( self, fmt,  rt ,   rd   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rd=name(self.CPR, rd)
        )
        self.CPR[rd] = self.GPR[rt]
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_ori( self, fmt,  rs ,   rt ,   immediate   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rs=name(self.GPR, rs), 
            immediate=immediate
        )
        self.GPR[rt] = self.GPR[rs] | immediate
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()

    def instr_andi( self, fmt,  rs ,   rt ,   immediate   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rs=name(self.GPR, rs), 
            immediate=immediate
        )
        self.GPR[rt] = self.GPR[rs] & immediate
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()        


    def instr_addu( self, fmt,  rs ,   rt ,   rd   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rs=name(self.GPR, rs), 
            rd=name(self.GPR, rd)
        )
        t = self.GPR[rs] + self.GPR[rt]
        #self.GPR[rt] = self.GPR[rs] & immediate
        self.GPR[rt] = t
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()        


    def instr_slti( self, fmt,  rs ,   rt ,   immediate   ):
        mne = fmt.format(
            rt=name(self.GPR, rt), 
            rs=name(self.GPR, rs), 
            immediate=immediate
        )
        self.GPR[rt] = 1 if self.GPR[rs] < immediate else 0
        self.notify(self.addr, self.opcode, f"{mne}")
        self.inc_pc()        
