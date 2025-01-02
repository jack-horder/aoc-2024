from dataclasses import dataclass
from typing import Self

@dataclass
class Coordinate:
    row:int
    column:int
    val:str = "X"

    def __add__(self, other:Self):
        return Coordinate(self.row + other.row, self.column + other.column, self.val)

    def __repr__(self) -> str:
        return self.val


@dataclass
class Word:
    val:str
    position:list[Coordinate]

def reflect_coordinate_in_x(coordinate: Coordinate) -> Coordinate:
    return Coordinate(-coordinate.row, coordinate.column)

def search_left(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.column - (len(word)-1) < 0:
        return None
    for i in range(len(word)):
        if grid[coordinate.row][coordinate.column - i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row, coordinate.column - i, word[i]) for i in range(len(word))])

def search_right(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.column + (len(word)) > len(grid[0]):
        return None
    for i in range(len(word)):
        if grid[coordinate.row][coordinate.column + i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row, coordinate.column + i, word[i]) for i in range(len(word))])

def search_up(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row - (len(word)-1) < 0:
        return None
    for i in range(len(word)):
        if grid[coordinate.row - i][coordinate.column] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row - i, coordinate.column, word[i]) for i in range(len(word))])

def search_down(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row + (len(word)-1) > len(grid):
        return None
    for i in range(len(word)):
        if grid[coordinate.row + i][coordinate.column] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row + i, coordinate.column, word[i]) for i in range(len(word))])

def search_up_left(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row - (len(word)-1) < 0 or coordinate.column - (len(word) -1) < 0:
        return None
    for i in range(len(word)):
        if grid[coordinate.row - i][coordinate.column - i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row - i, coordinate.column - i, word[i]) for i in range(len(word))])

def search_up_right(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row - (len(word)-1) < 0 or coordinate.column + len(word) > len(grid[0]):
        return None
    for i in range(len(word)):
        if grid[coordinate.row - i][coordinate.column + i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row - i, coordinate.column + i, word[i]) for i in range(len(word))])

def search_down_left(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row + (len(word)-1) > len(grid) or coordinate.column - (len(word)-1) < 0:
        return None
    for i in range(len(word)):
        if grid[coordinate.row + i][coordinate.column - i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row + i, coordinate.column - i, word[i]) for i in range(len(word))])

def search_down_right(word: str, coordinate: Coordinate, grid: list[list[str]]) -> Word | None:
    if coordinate.row + (len(word)-1) > len(grid) or coordinate.column + len(word) > len(grid[0]):
        return None
    for i in range(len(word)):
        if grid[coordinate.row + i][coordinate.column + i] != word[i]:
            return None
    return Word(word, [Coordinate(coordinate.row + i, coordinate.column + i, word[i]) for i in range(len(word))])



def search_words_at_pos(word: str, coordinate: Coordinate, grid:list[list[str]]) -> list[Word]:
    sl = search_left(word, coordinate, grid)
    sr = search_right(word, coordinate, grid)
    su = search_up(word, coordinate, grid)
    sd = search_down(word, coordinate, grid)
    sul = search_up_left(word, coordinate, grid)
    sur = search_up_right(word, coordinate, grid)
    sdl = search_down_left(word, coordinate, grid)
    sdr = search_down_right(word, coordinate, grid)

    all_searches = [sl, sr, su, sd, sul, sur, sdl, sdr]
    return [search for search in all_searches if search]

def get_blank_grid(grid:list[list[str]]) -> list[list[Coordinate]]:
    return [[Coordinate(x, y, ".") for y in range(len(grid[0]))] for x in range(len(grid))]

def overlay_words_on_grid(words:list[Word], grid:list[list[Coordinate]]) -> list[list[Coordinate]]:
    for word in words:
        for i in range(len(word.position)):
            grid[word.position[i].row][word.position[i].column] = word.position[i]
    return grid

def parse_puzzle_input():
    with open("day_4/puzzle_input.txt", "r") as file:
        return [list(line.strip()) for line in file.readlines()]

def parse_grid_coordinates(grid:list[list[str]]) -> list[list[Coordinate]]:
    return [[Coordinate(x, y, grid[x][y]) for y in range(len(grid[0]))] for x in range(len(grid))]

def p1():
    grid = parse_puzzle_input()
    words = ["XMAS"]
    words_found:list[Word] = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for word in words:
                words_found += search_words_at_pos(word, Coordinate(i, j), grid)
    print("Day 4 Part 1:")
    populated_grid = overlay_words_on_grid(words_found, get_blank_grid(grid))
    for row in populated_grid:
        print("".join(str(row)))
    print("\n")
    print(len(words_found))

def generate_combinations() -> list[str]:
    letters = ['M', 'S']
    combinations:list[str] = []

    for first in letters:
        for last in letters:
            combinations.append(f"{first}A{last}")

    return combinations

def validate_coordinate(rel_coordinates: list[Coordinate], coordinate: Coordinate, grid:list[list[Coordinate]], word:str) -> tuple[bool, list[Coordinate]]:
    absolute_coordinates = [coordinate + pos for pos in rel_coordinates]
    for pos in absolute_coordinates:
        if pos.row < 0 or pos.column < 0:
            return False, []
    for pos in absolute_coordinates:
        if pos.column >= (len(grid[0])) or pos.row >= (len(grid)):
            return False, []
    for i in range(len(word)):
        if grid[absolute_coordinates[i].row][absolute_coordinates[i].column].val != word[i]:
            return False, []
    for pos in absolute_coordinates:
        pos.val = grid[pos.row][pos.column].val
    return True, absolute_coordinates

def check_if_valid_coordinate(coordinate: Coordinate, grid:list[list[Coordinate]]) -> tuple[bool, list[Coordinate]]:
    combination_groups = [("MAS", "MAS"), ("SAS", "MAM"), ("SAM", "SAM"), ("MAM", "SAS")]
    valid_rel_coordinates = [Coordinate(-1, -1), Coordinate(0, 0), Coordinate(-1, 1)]
    valid_reflected_coordinates = [reflect_coordinate_in_x(coordinate) for coordinate in valid_rel_coordinates]
    is_valid = False
    is_valid_reflected = False
    valid_coordinates:list[Coordinate] = []
    for group in combination_groups:
        is_valid, coordinates = validate_coordinate(valid_rel_coordinates, coordinate, grid, group[0])
        if is_valid:
            valid_coordinates += coordinates
            is_valid_reflected, reflected_coordinates = validate_coordinate(valid_reflected_coordinates, coordinate, grid, group[1])
            if is_valid_reflected:
                valid_coordinates += reflected_coordinates
                return ((is_valid and is_valid_reflected), valid_coordinates)
        valid_coordinates = []
    return False, []


def p2_test():
    valid_rel_coordinates = [Coordinate(-1, -1), Coordinate(0, 0), Coordinate(-1, 1)]
    reflected_coordinates = [reflect_coordinate_in_x(coordinate) for coordinate in valid_rel_coordinates]
    empty_grid = get_blank_grid([["." for _ in range(9)] for _ in range(9)])
    for coordinates in [valid_rel_coordinates, reflected_coordinates]:
        for coordinate, letter in zip(coordinates, list("MAS")):
            absolute_point = Coordinate(2, 2, letter) + coordinate
            empty_grid[absolute_point.row][absolute_point.column] = absolute_point
    for row in empty_grid:
        print("".join([str(c) for c in row]))
    if check_if_valid_coordinate(empty_grid[2][2], empty_grid):
        print("Valid Coordinate")
    else:
        print("Not Valid Coordinate")

def add_coordinates_to_grid(grid:list[list[Coordinate]], coordinates: list[Coordinate]) -> list[list[Coordinate]]:
    for coordinate in coordinates:
        grid[coordinate.row][coordinate.column] = coordinate
    return grid

def p2():
    sum_of_valid_coordinates = 0
    grid = parse_puzzle_input()
    parsed_grid = parse_grid_coordinates(grid)
    blank_grid = get_blank_grid(grid)
    for row in parsed_grid:
        for coordinate in row:
            is_valid, coordinates = check_if_valid_coordinate(coordinate, parsed_grid)
            if is_valid:
                sum_of_valid_coordinates += 1
                blank_grid = add_coordinates_to_grid(blank_grid, coordinates)
    for row in blank_grid:
        print("".join([str(c) for c in row]))
    print("Day 4 Part 2:")
    print(sum_of_valid_coordinates)



def main():
    # p1()
    p2()


if __name__ == "__main__":
    main()
