"""CPU functionality."""

import sys
from numbers import Number


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [None] * 256
        self.reg = [None] * 8
        self.pc = 0

    def load(self, program):
        """Load a program into memory."""

        address = 0

        try:
            with open(program) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_num = comment_split[0]

                    if possible_num == '':
                        continue

                    if possible_num[0] == '1' or possible_num[0] == '0':
                        num = possible_num[:8]
                        self.ram[address] = int(num, 2)
                        address += 1

        except:
            print("Program not found.")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        # print()

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            IR = self.ram[self.pc]

            # HLT
            if IR == int('00000001', 2):
                running = False
                self.pc = 0

            # LDI
            if IR == int('10000010', 2):
                index = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[index] = value
                self.pc += 3

            # PRN
            if IR == int('01000111', 2):
                index = self.ram[self.pc + 1]
                value = self.reg[index]
                print(value)
                self.pc += 2

            # MUL
            if IR == int('10100010', 2):
                indexA = self.ram[self.pc + 1]
                indexB = self.ram[self.pc + 2]
                self.reg[indexA] = self.reg[indexA] * self.reg[indexB]
                self.pc += 3
