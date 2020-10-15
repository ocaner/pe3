# pe3

pe3 is an abbreviation for *python emotion engine emulator*, basically a python PS2 emulator.
Currently only consists of an code generator and PyQT based basic debugger. It just supports the R5900 CPU **19 instructions**, BIOS and RAM. Boot loops into the BIOS in the debugger.

## CPU Instructions

All supported instructions are stored and described in the `instructions.yml`.
To regenerate the instruction parser `R5900Gen.py` after an update on `instructions.yml` just run:

```console
python instructions.py > R5900Gen.py
```

The logic for the instruction needs to be implemented in `cpu.py` as method with the naming scheme `instr_<INSTRUCTION_NAME>` with at least one argument `fmt` and additional arguments for the instruction, see example [SW](cpu.py#L501) instruction:

```python
class R5900(R5900Gen):

    def instr_<INSTRUCTION_NAME>(self, fmt [, ...] ):
        pass
```

## Todo

* [ ] documentation for `instructions.yml`
* [ ] keyboard/gamepad input
* [ ] DVD drive
* [ ] GS
* [ ] VU