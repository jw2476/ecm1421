def readall(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
    
def writeall(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)

def parse_puzzle(puzzle: str) -> list[str]:
    puzzle = ''.join(puzzle.split('\n')[1:]) # discard first line

    parsed = []
    for character in puzzle:
        parsed.append(' ' if character == '0' else character)

    return parsed

def vjoin(blocks: list[list[str]]) -> list[str]:
    return [line for block in blocks for line in block]

def hjoin(blocks: list[list[str]]) -> list[str]:
    output = []

    for line in range(0, len(blocks[0])):
        output.append("".join([block[line] for block in blocks]))

    return output

def fmt_number(input: str, number: str) -> str:
    if input == " " or input == number:
        return number
    
    return " "

def fmt_square(input: str) -> list[str]:
    numbers = [fmt_number(input, str(number)) for number in range(1, 10)]
    return [
        " ".join(numbers[0:3]),
        " ".join(numbers[3:6]),
        " ".join(numbers[6:9]),
    ]

def fmt_tri(input: list[str]) -> list[str]:
    separator = [" | "] * 3
    return hjoin([
        fmt_square(input[0]), 
        separator, 
        fmt_square(input[1]), 
        separator, 
        fmt_square(input[2])
    ])


def format_row(input: list[str]) -> list[str]:
    return hjoin([
        ["|| "] * 3,
        fmt_tri(input[0:3]),
        [" || "] * 3,
        fmt_tri(input[3:6]),
        [" || "] * 3,
        fmt_tri(input[6:9]),
        [" ||"] * 3
    ])

def format_tri_row(input: list[str]) -> list[str]:
    separator = ["-" * 77]
    return vjoin([
        format_row(input[0:9]),
        separator,
        format_row(input[9:18]),
        separator,
        format_row(input[18:27])
    ])

def format_puzzle(puzzle: list[str]) -> str:
    separator = ["=" * 77]
    output = vjoin([
        separator,
        format_tri_row(puzzle[0:27]),
        separator,
        format_tri_row(puzzle[27:54]),
        separator,
        format_tri_row(puzzle[54:81]),
        separator,
    ])

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