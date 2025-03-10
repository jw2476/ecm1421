from pathlib import Path
from typing import List

def readall(path: Path) -> str:
    with open(path, 'r') as f:
        return f.read()
    
def writeall(path: Path, content: str):
    with open(path, 'w') as f:
        f.write(content)

def parse_puzzle(puzzle: str) -> List[str]:
    puzzle = ''.join(puzzle.split('\n')[1:]) # discard first line

    parsed = []
    for character in puzzle:
        parsed.append(' ' if character == '0' else character)

    return parsed

def fmt_tri(input: List[str]) -> str:
    return f" {input[0]} {input[1]} {input[2]} "

def format_row(input: List[str]) -> str:
    return f" |{fmt_tri(input[0:3])}|{fmt_tri(input[3:6])}|{fmt_tri(input[6:9])}|"

def format_puzzle(puzzle: List[str]) -> str:
    SEPARATOR: str = "--------------------------"
    
    output = [
        SEPARATOR,
        format_row(puzzle[0:9]),
        format_row(puzzle[9:18]),
        format_row(puzzle[18:27]),
        SEPARATOR,
        format_row(puzzle[27:36]),
        format_row(puzzle[36:45]),
        format_row(puzzle[45:54]),
        SEPARATOR,
        format_row(puzzle[54:63]),
        format_row(puzzle[63:72]),
        format_row(puzzle[72:81]),
        SEPARATOR
    ]

    return '\n'.join(output)


def test():
    output = format_puzzle(parse_puzzle(readall("example.txt")))
    print(output)
    assert(output == readall("1a.txt"))

def choose_puzzle() -> int:
    while True:
        try:
            selected = int(input("Please choose a sudoku puzzle (1-10): "))
            if 1 <= selected <= 10:
                return selected
        except:
            pass

        print("Valid puzzles are numbered 1-10 so please enter a number between 1 and 10") 

def main():
    puzzle_number = choose_puzzle()
    puzzle_text = readall(f"puzzles/sudoku_grid{puzzle_number:02}.txt")
    puzzle = parse_puzzle(puzzle_text)
    formatted = format_puzzle(puzzle)
    writeall("puzzleBlank.txt", formatted)
    print("Written to puzzleBlank.txt")


if __name__ == "__main__":
    main()