   
from typing import Mapping

# TODO: Decorator to make rules creation easier


class Emulator():
    """
    Emulator emulates arbitary asm-like construction.
    """

    memory: bytes
    "memory of the code"
    registers: list[str]
    "list of registers"
    registers_map: Mapping[str, int]
    "map storing registers value"
    instruction_pointer_name: str
    "storing name of the register storing instruction pointer"    
    rules: list[any]
    "list of rules to tranform state"
    ending_conditions: list[any]
    "list of ending condition to complete transformation"

    def __init__(self, memory):
        self.memory = memory
        self.rules = []
        self.ending_conditions = []
        self.registers = []
        self.registers_map = {}

    def set_registers(self, registers: list[str]):
        self.registers = registers
        self.registers_map = {}
        for reg in self.registers:
            self.registers_map[reg] = 0

    def set_register(self, register: str, value: int):
        """Set the state of the register"""
        self.registers_map[register] = value

    def set_instruction_pointer(self, register: str):
        """Set the name of the instruction pointer"""
        self.instruction_pointer_name = register

    def set_transformer(self, transformer):
        self.transformer = transformer

    def add_rule(self, rule):
        """
        Add a rule to transform code.
        Usually this is one block of function emulating the behaviour of one specific instruction

        Rules: (emulator) => (is_transformed)
        """
        self.rules.append(rule)

    def add_ending_condition(self, rule):
        """
        Add an ending condition for code emulation
        This is also a rule.
        """
        self.ending_conditions.append(rule)

    def emulate(self):
        """
        emulate the whole program
        """
        while True:
            executed = self.step()
            if not executed:
                break

    def step(self) -> bool:
        """
        Step an rule. Returns an bool representing whether the step occurs.
        If the step do not occurs, the program comes to an end as indicated by ending conditions.

        raise NotImplementedError if rule to apply could not be found.
        """
        for rule in self.ending_conditions:
            result = rule(self)
            if result:
                return False

        is_transformed = False
        for rule in self.rules:
            result = rule(self)
            if result:
                is_transformed = True
                break
        if not is_transformed:
            raise NotImplementedError("no rules applied")
        return True


# Usage?
e = Emulator()
e.add_extractor(lambda: mem[ip] >> 4)
e.add_rule(add)
