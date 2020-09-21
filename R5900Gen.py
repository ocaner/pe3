from opcodes import OpCodes

class R5900Gen(OpCodes):

    def opcode_hook(self):

        # TLBWI 
        if self.opcode & 0xffffffff == 0x42000002:
            self.instr_tlbwi(  )
            return True

        # BNE  rs ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0x14000000:
            self.instr_bne( self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SD  base ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0xfc000000:
            self.instr_sd( self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SW  base ,   rt ,   offset  
        if self.opcode & 0xfc000000 == 0xac000000:
            self.instr_sw( self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # JAL  instr_index  
        if self.opcode & 0xfc000000 == 0xc000000:
            self.instr_jal( self.opcode & 0x3ffffff << 2  )
            return True

        # JR  rs  
        if self.opcode & 0xfc00003f == 0x8:
            self.instr_jr( self.opcode & 0x3e00000 >> 21  )
            return True

        # JALR  rs ,   rd  
        if self.opcode & 0xfc00003f == 0x9:
            self.instr_jalr( self.opcode & 0x3e00000 >> 21 , self.opcode & 0xf800 >> 11  )
            return True

        # SYNC  stype  
        if self.opcode & 0xfffff83f == 0xf:
            self.instr_sync( self.opcode & 0x7c0 >> 6  )
            return True

        # LI  rt ,   val  
        if self.opcode & 0x3f000000 == 0x24000000:
            self.instr_li( self.opcode & 0xff0000 >> 16 , self.opcode & 0xffff )
            return True

        # LUI  rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x3c000000:
            self.instr_lui( self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff << 16  )
            return True

        # MFC0  rt ,   rd  
        if self.opcode & 0xffe007ff == 0x40000000:
            self.instr_mfc0( self.opcode & 0x1f0000 >> 16 , self.opcode & 0xf800 >> 11  )
            return True

        # MFC1  rt ,   fs  
        if self.opcode & 0xffe007ff == 0x44000000:
            self.instr_mfc1( self.opcode & 0x1f0000 >> 15 , self.opcode & 0xf800 >> 10  )
            return True

        # MTC0  rt ,   rd  
        if self.opcode & 0xffe007ff == 0x40800000:
            self.instr_mtc0( self.opcode & 0x1f0000 >> 16 , self.opcode & 0xf800 >> 11  )
            return True

        # ORI  rs ,   rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x34000000:
            self.instr_ori( self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # SLTI  rs ,   rt ,   immediate  
        if self.opcode & 0xfc000000 == 0x28000000:
            self.instr_slti( self.opcode & 0x3e00000 >> 21 , self.opcode & 0x1f0000 >> 16 , self.opcode & 0xffff )
            return True

        # XXX error handling
        self.error(self.addr, self.opcode, None, "UNKNOWN OP CODE")
        return False


    def instr_tlbwi( self,  ):
         """TLBWI 

        Mask   : 11111111111111111111111111111111
        OPCODE : 01000010000000000000000000000010

        Arguments:
        
        """
        pass

    def instr_bne( self,  rs ,   rt ,   offset   ):
         """BNE  rs ,   rt ,   offset  

        Mask   : 11111100000000000000000000000000
        OPCODE : 00010100000000000000000000000000

        Arguments:
         
        1. rs
        Mask   : 00000011111000000000000000000000
         
        2. rt
        Mask   : 00000000000111110000000000000000
         
        3. offset
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_sd( self,  base ,   rt ,   offset   ):
         """SD  base ,   rt ,   offset  

        Mask   : 11111100000000000000000000000000
        OPCODE : 11111100000000000000000000000000

        Arguments:
         
        1. base
        Mask   : 00000011111000000000000000000000
         
        2. rt
        Mask   : 00000000000111110000000000000000
         
        3. offset
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_sw( self,  base ,   rt ,   offset   ):
         """SW  base ,   rt ,   offset  

        Mask   : 11111100000000000000000000000000
        OPCODE : 10101100000000000000000000000000

        Arguments:
         
        1. base
        Mask   : 00000011111000000000000000000000
         
        2. rt
        Mask   : 00000000000111110000000000000000
         
        3. offset
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_jal( self,  instr_index   ):
         """JAL  instr_index  

        Mask   : 11111100000000000000000000000000
        OPCODE : 00001100000000000000000000000000

        Arguments:
         
        1. instr_index
        Mask   : 00000011111111111111111111111111
        
        """
        pass

    def instr_jr( self,  rs   ):
         """JR  rs  

        Mask   : 11111100000000000000000000111111
        OPCODE : 00000000000000000000000000001000

        Arguments:
         
        1. rs
        Mask   : 00000011111000000000000000000000
        
        """
        pass

    def instr_jalr( self,  rs ,   rd   ):
         """JALR  rs ,   rd  

        Mask   : 11111100000000000000000000111111
        OPCODE : 00000000000000000000000000001001

        Arguments:
         
        1. rs
        Mask   : 00000011111000000000000000000000
         
        2. rd
        Mask   : 00000000000000001111100000000000
        
        """
        pass

    def instr_sync( self,  stype   ):
         """SYNC  stype  

        Mask   : 11111111111111111111100000111111
        OPCODE : 00000000000000000000000000001111

        Arguments:
         
        1. stype
        Mask   : 00000000000000000000011111000000
        
        """
        pass

    def instr_li( self,  rt ,   val   ):
         """LI  rt ,   val  

        Mask   : 00111111000000000000000000000000
        OPCODE : 00100100000000000000000000000000

        Arguments:
         
        1. rt
        Mask   : 00000000111111110000000000000000
         
        2. val
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_lui( self,  rt ,   immediate   ):
         """LUI  rt ,   immediate  

        Mask   : 11111100000000000000000000000000
        OPCODE : 00111100000000000000000000000000

        Arguments:
         
        1. rt
        Mask   : 00000000000111110000000000000000
         
        2. immediate
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_mfc0( self,  rt ,   rd   ):
         """MFC0  rt ,   rd  

        Mask   : 11111111111000000000011111111111
        OPCODE : 01000000000000000000000000000000

        Arguments:
         
        1. rt
        Mask   : 00000000000111110000000000000000
         
        2. rd
        Mask   : 00000000000000001111100000000000
        
        """
        pass

    def instr_mfc1( self,  rt ,   fs   ):
         """MFC1  rt ,   fs  

        Mask   : 11111111111000000000011111111111
        OPCODE : 01000100000000000000000000000000

        Arguments:
         
        1. rt
        Mask   : 00000000000111110000000000000000
         
        2. fs
        Mask   : 00000000000000001111100000000000
        
        """
        pass

    def instr_mtc0( self,  rt ,   rd   ):
         """MTC0  rt ,   rd  

        Mask   : 11111111111000000000011111111111
        OPCODE : 01000000100000000000000000000000

        Arguments:
         
        1. rt
        Mask   : 00000000000111110000000000000000
         
        2. rd
        Mask   : 00000000000000001111100000000000
        
        """
        pass

    def instr_ori( self,  rs ,   rt ,   immediate   ):
         """ORI  rs ,   rt ,   immediate  

        Mask   : 11111100000000000000000000000000
        OPCODE : 00110100000000000000000000000000

        Arguments:
         
        1. rs
        Mask   : 00000011111000000000000000000000
         
        2. rt
        Mask   : 00000000000111110000000000000000
         
        3. immediate
        Mask   : 00000000000000001111111111111111
        
        """
        pass

    def instr_slti( self,  rs ,   rt ,   immediate   ):
         """SLTI  rs ,   rt ,   immediate  

        Mask   : 11111100000000000000000000000000
        OPCODE : 00101000000000000000000000000000

        Arguments:
         
        1. rs
        Mask   : 00000011111000000000000000000000
         
        2. rt
        Mask   : 00000000000111110000000000000000
         
        3. immediate
        Mask   : 00000000000000001111111111111111
        
        """
        pass

