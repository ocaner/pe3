# pe3

pe3 is an abbreviation for *python emotion engine emulator*, basically a python PS2 emulator.
Currently just supports the R5900 CPU **only 19 instructions**, BIOS and RAM.

## CPU Instructions

All supported instructions are stored in the `instructions.yml`.
To regenerate the instruction parser `R5900Gen.py` after an update on `instructions.yml` just run:

```console
python instructions.py > R5900Gen.py
```

The logic for the instruction needs to be implemented in `cpu.py` as method with the naming scheme `instr_<INSTRUCTION_NAME>` with at least one argument `fmt` and additional arguments for the instruction, see example [SW](cpu.py#L501) instruction.


## Todo

* [ ] keyboard/gamepad input
* [ ] DVD drive
* [ ] GS
* [ ] VU