#!/usr/bin/env python3

from mmap import mmap, MAP_PRIVATE, PROT_READ
from struct import calcsize, unpack_from

class ROMDir:
    FORMAT = "10sHI"
    
    name = None

    ext_info_size = None

    file_size = None

class BIOS:

    def __init__(self, path):
        self.path = path
        self.fo = open(self.path, "rb")

        self.map = mmap(self.fo.fileno(), 0, MAP_PRIVATE, PROT_READ)
        self.size = len(self.map)
        self.data_offset = -1
        self.files = {}
        self.index()


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
        while not eof:
            p = unpack_from(ROMDir.FORMAT, self.map, idx)

            if p[0] == term and p[1] == 0 and p[2] == 0:
                break
            
            rd = ROMDir()
            rd.name = p[0].decode("ascii").replace(chr(0), "")
            rd.ext_info_size = p[1]
            rd.file_size = p[2]

            if rd.name not in self.files:
                self.files[rd.name] = []

            self.files[rd.name].append(rd)

            print(f"{i}. {idx:04x} ROMDIR => {rd.name} {rd.ext_info_size} {rd.file_size}")

            i += 1
            idx += size #+ p[1] + p[2]
        
        self.data_offset = idx

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
