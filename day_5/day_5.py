from dataclasses import dataclass

@dataclass
class Rule:
    first:int
    second:int


def parse_puzzle_input(file_name:str) -> list[str]:
    with open(file_name, "r") as file:
        return [line.strip() for line in file.readlines()]

def parse_puzzle_rules(puzzle_input:list[str]) -> list[Rule]:
    break_index = puzzle_input.index("")
    puzzle_rules = puzzle_input[:break_index]
    return [Rule(int(line.split("|")[0]), int(line.split("|")[1])) for line in puzzle_rules]

def parse_puzzle_page_updates(puzzle_input:list[str]) -> list[list[int]]:
    break_index = puzzle_input.index("")
    puzzle_page_updates = puzzle_input[break_index+1:]
    return [[int(num) for num in line.split(",")] for line in puzzle_page_updates]

def main():
    # puzzle_input = parse_puzzle_input("day_5/puzzle_input.txt")
    # rules = parse_puzzle_rules(puzzle_input)
    # page_updates = parse_puzzle_page_updates(puzzle_input)
    # print(page_updates)
    # print(rules)
    p1()


def get_middle_page_number(page_update: list[int]) -> int:
    middle_index = len(page_update) // 2
    return page_update[middle_index]

def get_rule(rules:list[Rule], page_numbers:tuple[int, int]):
    for rule in rules:
        if rule.first == page_numbers[0]:
            if rule.second == page_numbers[1]:
                return rule
        if rule.first == page_numbers[1]:
            if rule.second == page_numbers[0]:
                return rule
    return None

def is_page_pair_order_valid(first: int, second:int, rules:list[Rule]) -> bool:
    rule = get_rule(rules=rules, page_numbers=(first, second))
    if not rule:
        return True
    if rule.first == first and rule.second == second:
        return True
    return False

def p1():
    puzzle_input = parse_puzzle_input("day_5/puzzle_input.txt")
    rules = parse_puzzle_rules(puzzle_input)
    page_updates = parse_puzzle_page_updates(puzzle_input)
    valid_middle_page_numbers: list[int] = []
    print("Day 5 Part 1:")
    for update in page_updates:
        valid = True
        for i in range(len(update)):
            if not i == len(update) - 1:
                if not is_page_pair_order_valid(update[i], update[i+1], rules):
                    print(f"Invalid page pair order: {update[i]} {update[i+1]}")
                    valid = False
                    break
        if valid:
            valid_middle_page_numbers.append(get_middle_page_number(update))
    print(sum(valid_middle_page_numbers))




if __name__ == "__main__":
    main()
