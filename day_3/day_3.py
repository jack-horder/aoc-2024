from dataclasses import dataclass
import re

@dataclass
class Instruction:
    operation: str
    num1: int
    num2: int
    enabled:bool = True

    def get_result(self) -> int:
        match self.operation:
            case "mul":
                return self.num1 * self.num2
            case _:
                return 0

    def get_enabled_result(self) -> int:
        if self.enabled:
            return self.get_result()
        return 0

def get_instructions(file_name:str) -> str:
    with open(file_name) as f:
        return f.read()

def parse_instruction(input:str) -> Instruction:
    numbers_pattern = r'\w+\((\d+),(\d+)\)'
    enabled_pattern = r"don't\(\)|do\(\)"
    if re.match(pattern=enabled_pattern, string=input):
        if re.match(pattern=r"do\(\)", string=input):
            return Instruction(operation="do", num1=0, num2=0, enabled=True)
        if re.match(pattern=r"don't\(\)", string=input):
            return Instruction(operation="don't", num1=0, num2=0, enabled=False)
    operation = re.match(pattern=r"^\w*", string=input)
    if operation is None:
        raise ValueError("operation not found")
    num1, num2 = map(int, re.findall(numbers_pattern, input)[0])
    return Instruction(
        operation=operation[0],
        num1=num1,
        num2=num2,
    )

def set_instructions_enabled(instructions:list[Instruction]):
    for idx, inst in enumerate(instructions):
        if idx == 0:
            inst.enabled = True
            continue
        if inst.operation not in ("do", "don't"):
            inst.enabled = instructions[idx-1].enabled


def day_3_p1():
    instructions = extract_instructions(input=get_instructions("day_3/puzzle_input.txt"))
    print(sum([inst.get_result() for inst in instructions]))

def day_3_p2():
    instructions = extract_instructions(input=get_instructions("day_3/puzzle_input.txt"))
    print(sum([inst.get_enabled_result() for inst in instructions]))

def extract_instructions(input:str) -> list[Instruction]:
    parsed_instructions:list[Instruction] = []
    pat = r"mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)"
    instructions = re.findall(pattern=pat, string=input)
    for instruction in instructions:
        parsed_instructions.append(parse_instruction(instruction))
    set_instructions_enabled(parsed_instructions)
    return parsed_instructions

def main():
    # part 1
    print("Day 3 Part 1")
    print("Answer:")
    day_3_p1()
    # part 2
    print("Day 3 Part 2")
    print("Answer:")
    day_3_p2()

if __name__ == "__main__":
    main()
