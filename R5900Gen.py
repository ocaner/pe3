from opcodes import OpCodes

class R5900Gen(OpCodes):

    def opcode_hook(self):

        # TLBWI 
        if self.opcode & 0xffffffff == 0x42000002:
            self.instr_tlbwi( "TLBWI ",  )
            return True

        # BNE  rs ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0x14000000:
            self.instr_bne( "BNE {rt}, {rs}, {offset:08x}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SD  base ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0xfc000000:
            self.instr_sd( "SD {rt}, {offset:08x} ( {base:08x} )", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SW  base ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0xac000000:
            self.instr_sw( "SW {rt}, {offset:08x} ( {base:08x} )", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # LW  base ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0x8c000000:
            self.instr_lw( "LW {rt}, {offset:08x} ( {base:08x} )", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # JAL  instr_index  
        if self.opcode & 0xfc000000 == 0xc000000:
            self.instr_jal( "JAL {instr_index:08x}", self.opcode & 0x3ffffff << 2  )
            return True

        # JR  rs  
        if self.opcode & 0xfc00003f == 0x8:
            self.instr_jr( "JR {rs}", self.opcode & 0x3e00000 >> 21  )
            return True

        # JALR  rs ,   rd  
        if self.opcode & 0xfc00003f == 0x9:
            self.instr_jalr( "JALR {rs}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0xf800 >> 11  )
            return True

        # SYNC  stype  
        if self.opcode & 0xfffff83f == 0xf:
            self.instr_sync( "SYNC {stype}", self.opcode & 0x7c0 >> 6  )
            return True

        # LI  rt ,   val  
        if self.opcode & 0x3f000000 == 0x24000000:
            self.instr_li( "LI {rt}, {val}", self.opcode & 0xff0000 >> 16 , self.opcode & 0xffff )
            return True

        # LUI  rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x3c000000:
            self.instr_lui( "LUI {rt}, {immediate:08x}", self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff << 16  )
            return True

        # MFC0  rt ,   rd  
        if self.opcode & 0xffe007ff == 0x40000000:
            self.instr_mfc0( "MFC0 {rt}, {rd}", self.opcode & 0x1f0000 >> 16 , self.opcode & 0xf800 >> 11  )
            return True

        # MFC1  rt ,   fs  
        if self.opcode & 0xffe007ff == 0x44000000:
            self.instr_mfc1( "MFC1 ", self.opcode & 0x1f0000 >> 15 , self.opcode & 0xf800 >> 10  )
            return True

        # MTC0  rt ,   rd  
        if self.opcode & 0xffe007ff == 0x40800000:
            self.instr_mtc0( "MTC0 {rt}, {rd}", self.opcode & 0x1f0000 >> 16 , self.opcode & 0xf800 >> 11  )
            return True

        # ADDU  rs ,   rt ,   rd  
        if self.opcode & 0xfc00003f == 0x21:
            self.instr_addu( "ADDU {rt}, {rs}, {rd}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xf800 >> 11  )
            return True

        # ANDI  rs ,   rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x30000000:
            self.instr_andi( "ANDI {rt}, {rs}, {immediate:04x}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # ORI  rs ,   rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x34000000:
            self.instr_ori( "ORI {rt}, {rs}, {immediate:04x}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SLTI  rs ,   rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x28000000:
            self.instr_slti( "SLTI {rt}, {rs}, {immediate:04x}", self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # XXX error handling
        self.error(self.addr, self.opcode, None, "UNKNOWN OP CODE")
        return False


    def instr_tlbwi( self, fmt,  ):
        
        pass

    def instr_bne( self, fmt,  rs ,   rt ,   offset   ):
        
        pass

    def instr_sd( self, fmt,  base ,   rt ,   offset   ):
        
        pass

    def instr_sw( self, fmt,  base ,   rt ,   offset   ):
        
        pass

    def instr_lw( self, fmt,  base ,   rt ,   offset   ):
        
        pass

    def instr_jal( self, fmt,  instr_index   ):
        
        pass

    def instr_jr( self, fmt,  rs   ):
        
        pass

    def instr_jalr( self, fmt,  rs ,   rd   ):
        
        pass

    def instr_sync( self, fmt,  stype   ):
        
        pass

    def instr_li( self, fmt,  rt ,   val   ):
        
        pass

    def instr_lui( self, fmt,  rt ,   immediate   ):
        
        pass

    def instr_mfc0( self, fmt,  rt ,   rd   ):
        
        pass

    def instr_mfc1( self, fmt,  rt ,   fs   ):
        
        pass

    def instr_mtc0( self, fmt,  rt ,   rd   ):
        
        pass

    def instr_addu( self, fmt,  rs ,   rt ,   rd   ):
        
        pass

    def instr_andi( self, fmt,  rs ,   rt ,   immediate   ):
        
        pass

    def instr_ori( self, fmt,  rs ,   rt ,   immediate   ):
        
        pass

    def instr_slti( self, fmt,  rs ,   rt ,   immediate   ):
        
        pass

