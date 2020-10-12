#!/usr/bin/env python3

from mmap import mmap, MAP_PRIVATE, PROT_READ
from struct import calcsize, unpack_from

class ROMDir:
    FORMAT = "10sHI"
    
    name = None

    ext_info_size = None

    file_size = None

    offset = None

ZONES = dict( T="T10K", X = "Test", J = "Japan", A = "USA", E = "Europe", H = "HK", P = "FREE", C = "China" ) 

class BIOS:

    def __init__(self, path):
        self.path = path
        self.fo = open(self.path, "rb")

        self.map = mmap(self.fo.fileno(), 0, MAP_PRIVATE, PROT_READ)
        self.size = len(self.map)
        self.data_offset = -1
        self.files = {}

        self.zone = None
        self.version = None
        self.version_str = None
        self.date = None
        self.additional = None

        self.index()

    def get_file(self, name):
        f = self.files.get(name)

        if f and len(f) == 1:
            f = f[0]
            content = self.read_buffer(f.offset, f.file_size)

        return f, content

    def index(self):
        a = "RESET"
        RESET = []
        for c in a:
            RESET.append(ord(c))
        print(f"BIOS INDEX => {RESET}")
        size = calcsize(ROMDir.FORMAT)
        #return 

        # search for first romdir
        idx = -1

        for i in range(len(self.map)):
            buf = self.read_buffer(i, 5)
            #s = "".join(buf).decode("ascii")
            #print(f"{i:04x} => {buf}")

            if RESET == buf:
                print("FOUND")
                idx = i
                break
        
        #b = bytearray(1024)
        #gen = iter_unpack(ROMDir.FORMAT, b)

        #for  in gen:
        eof = False
        term = b"\x00" * 10
        i = 1
        offset = 0
        while not eof:
            p = unpack_from(ROMDir.FORMAT, self.map, idx)

            if p[0] == term and p[1] == 0 and p[2] == 0:
                break
            
            rd = ROMDir()
            rd.name = p[0].decode("ascii").replace(chr(0), "")
            rd.ext_info_size = p[1]
            rd.file_size = p[2]
            rd.offset = offset

            if rd.name == "ROMVER":
                romver = unpack_from("14s", self.map, rd.offset)[0].decode("ascii")
                
                print(f"ROMVER => {romver}")
                zonefail = romver[4]
                self.zone = ZONES.get(zonefail, zonefail)
                vermaj = romver[0:1]
                vermin = romver[2:3]

                self.version_str = f"v{vermaj:s}.{vermin:s}"
                self.date = f"{romver[12:14]}/{romver[10:12]}/{romver[6:10]}"
                
                self.additional = "Console" if romver[5] == "C" else "Devel" if romver[5] == "D" else "" 
                
                self.version = int(vermaj) << 8 | int(vermin)
                
                print(f"{self.zone:7s} {self.version_str} ({self.date}) {self.additional} {self.version} {self.version:08x}")


            if rd.name not in self.files:
                self.files[rd.name] = []

            self.files[rd.name].append(rd)

            print(f"{i}. {idx:04x} ROMDIR => {rd.name} {rd.ext_info_size} ( {rd.ext_info_size:04x} ) {rd.file_size} ( {rd.file_size:08x} ) {rd.offset:08x}")

            i += 1
            idx += size #+ p[1] + p[2]
            
            if rd.file_size % 0x10 == 0:
                offset += rd.file_size
            else:
                offset += (rd.file_size + 0x10) & 0xfffffff0

        self.data_offset = idx

        # XXX load extra roms: rom1, rom2, erom

        # XXX load irx

        # XXX checksum

    def load_extra_rom(self, name, addr):
        pass

    def checksum(self):
        s = 4
        result = 0

        for i in range(0, self.size, s):
            result = result ^ unpack_from("<I", self.map[i:i + 5])[0]

        return result

    def close(self):
        self.map.close()

    def read_buffer(self, addr, l):
        buf = []

        for i in range(l):
            buf.append(self.map[addr + i])
        
        return buf

    def read(self, addr):
        return self.map[addr]

    def read_qword(self, addr):
        return self.map[addr:addr+4]
