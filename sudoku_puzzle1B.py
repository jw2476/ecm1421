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


def vjoin(blocks: list[list[str]]) -> list[str]:
    """
    Joins a list of blocks vertically.

    Args:
        blocks (list[list[str]]): The list of blocks.

    Returns:
        list[str]: The vertically joined blocks.
    """
    return [line for block in blocks for line in block]


def hjoin(blocks: list[list[str]]) -> list[str]:
    """
    Joins a list of blocks horizontally.

    Args:
        blocks (list[list[str]]): The list of blocks.

    Returns:
        list[str]: The horizontally joined blocks.
    """
    output = []

    for line in range(0, len(blocks[0])):
        output.append("".join([block[line] for block in blocks]))

    return output


def fmt_number(input: str, number: str) -> str:
    """
    Formats a number in a square.

    Args:
        input (str): The input number for the square.
        number (str): The number to show on the square.

    Returns:
        str: The number if it should be shown.
    """
    if input == " " or input == number:
        return number

    return " "


def fmt_square(input: str) -> list[str]:
    """
    Formats a square from the input.

    Args:
        input (str): The input number for the square.

    Returns:
        list[str]: The formatted lines.
    """
    numbers = [fmt_number(input, str(number)) for number in range(1, 10)]
    return [
        " ".join(numbers[0:3]),
        " ".join(numbers[3:6]),
        " ".join(numbers[6:9]),
    ]


def fmt_tri(input: list[str]) -> list[str]:
    """
    Formats 3 numbers from the input.

    Args:
        input (list[str]): The 3 input numbers.

    Returns:
        list[str]: The formatted lines.
    """
    separator = [" | "] * 3
    return hjoin(
        [
            fmt_square(input[0]),
            separator,
            fmt_square(input[1]),
            separator,
            fmt_square(input[2]),
        ]
    )


def format_row(input: list[str]) -> list[str]:
    """
    Formats a row from the input.

    Args:
        input (list[str]): The row numbers.

    Returns:
        list[str]: The formatted lines.
    """
    return hjoin(
        [
            ["|| "] * 3,
            fmt_tri(input[0:3]),
            [" || "] * 3,
            fmt_tri(input[3:6]),
            [" || "] * 3,
            fmt_tri(input[6:9]),
            [" ||"] * 3,
        ]
    )


def format_tri_row(input: list[str]) -> list[str]:
    """
    Formats 3 rows from the input.

    Args:
        input (list[str]): The rows.

    Returns:
        list[str]: The formatted lines.
    """
    separator = ["-" * 77]
    return vjoin(
        [
            format_row(input[0:9]),
            separator,
            format_row(input[9:18]),
            separator,
            format_row(input[18:27]),
        ]
    )


def format_puzzle(puzzle: list[str]) -> str:
    """
    Formats a puzzle.

    Args:
        puzzle (list[str]): The puzzle.

    Returns:
        str: The formatted string.
    """
    separator = ["=" * 77]
    output = vjoin(
        [
            separator,
            format_tri_row(puzzle[0:27]),
            separator,
            format_tri_row(puzzle[27:54]),
            separator,
            format_tri_row(puzzle[54:81]),
            separator,
        ]
    )

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
