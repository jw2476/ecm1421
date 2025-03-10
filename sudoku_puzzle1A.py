def readall(path: str) -> str:
    """
    Reads an entire file.

    Args:
        path (str): The path of the file.

    Returns:
        (str): The contents of the file.
    """
    with open(path, "r") as f:
        return f.read()


def writeall(path: str, content: str) -> None:
    """
    Writes a string to a file. This will create a file if one does not exist, or overwrite the file if it exists.

    Args:
        path (str): The path of the file.
        content (str): The content to write the file.
    """
    with open(path, "w") as f:
        f.write(content)


def parse_puzzle(puzzle: str) -> list[str]:
    """
    Parse the puzzle into a 1D list of characters.

    Args:
        puzzle (str): The raw puzzle string.

    Returns:
        list[str]: The 1D list of characters.
    """
    puzzle = "".join(puzzle.split("\n")[1:])  # discard first line

    parsed = []
    for character in puzzle:
        parsed.append(" " if character == "0" else character)

    return parsed


def format_tri(input: list[str]) -> str:
    """
    Formats 3 numbers from the input.

    Args:
        input (list[str]): The 3 input numbers.

    Returns:
        str: The formatted string.
    """
    return f" {input[0]} {input[1]} {input[2]} "


def format_row(input: list[str]) -> str:
    """
    Formats a row from the input.

    Args:
        input (list[str]): The row numbers.

    Returns:
        str: The formatted string.
    """
    return (
        f" |{format_tri(input[0:3])}|{format_tri(input[3:6])}|{format_tri(input[6:9])}|"
    )


def format_puzzle(puzzle: list[str]) -> str:
    """
    Formats a puzzle.

    Args:
        puzzle (list[str]): The puzzle.

    Returns:
        str: The formatted string.
    """
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
        SEPARATOR,
    ]

    return "\n".join(output)


def choose_puzzle() -> int:
    """
    Gets a user chosed puzzle index.

    Returns:
        int: The chosen puzzle index.
    """
    while True:
        try:
            selected = int(input("Please choose a sudoku puzzle (1-10): "))
            if 1 <= selected <= 10:
                return selected
        except:
            pass

        print(
            "Valid puzzles are numbered 1-10 so please enter a number between 1 and 10"
        )


def main():
    """
    Gets the user to choose a puzzle, then formats and writes it out to puzzleBlank.txt.
    """
    puzzle_number = choose_puzzle()
    puzzle_text = readall(f"puzzles/sudoku_grid{puzzle_number:02}.txt")
    puzzle = parse_puzzle(puzzle_text)
    formatted = format_puzzle(puzzle)
    writeall("puzzleBlank.txt", formatted)
    print("Written to puzzleBlank.txt")


if __name__ == "__main__":
    main()
