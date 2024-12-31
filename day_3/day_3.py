from dataclasses import dataclass
import re

@dataclass
class Instruction:
    operation: str
    num1: int
    num2: int

    def get_result(self) -> int:
        match self.operation:
            case "mul":
                return self.num1 * self.num2
            case _:
                raise TypeError("instruction type not recognizned")

def get_instructions(file_name:str) -> str:
    with open(file_name) as f:
        return f.read()

def parse_instruction(input:str) -> Instruction:
    numbers_pattern = r'\w+\((\d+),(\d+)\)'
    operation = re.match(pattern=r"^\w*", string=input)
    if operation is None:
        raise ValueError("operation not found")
    num1, num2 = map(int, re.findall(numbers_pattern, input)[0])
    return Instruction(
        operation=operation[0],
        num1=num1,
        num2=num2,
    )


def day_3_p1():
    instructions = extract_instructions(input=get_instructions("day_3/puzzle_input.txt"))
    print(sum([inst.get_result() for inst in instructions]))

def extract_instructions(input:str) -> list[Instruction]:
    parsed_instructions:list[Instruction] = []
    pat = r"mul\(\d{1,3},\d{1,3}\)"
    instructions = re.findall(pattern=pat, string=input)
    for instruction in instructions:
        parsed_instructions.append(parse_instruction(instruction))
    return parsed_instructions

def main():
    print("Day 3 Part 1")
    print("Answer:")
    day_3_p1()

if __name__ == "__main__":
    main()
