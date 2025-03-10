from pprint import pprint
from matplotlib import pyplot as plt


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


def parse_csv_line(line: str) -> list[str]:
    """
    Parses a CSV line.

    Args:
        line (str): The comma-separated line to parse.

    Returns:
        list[str]: The comma-separated entries in the line.
    """
    row: list[str] = []
    pointer: int = 0

    while pointer < len(line):
        if line[pointer] == '"':
            pointer += 1
            cell = line[pointer:].split('"')[0]  # get all text in string
            pointer += len(cell) + 2  # advance pointer by length of text plus ",
            row.append(cell)
        else:
            cell = line[pointer:].split(",")[0]
            pointer += len(cell) + 1  # advance pointer by length of cell plus ,
            row.append(cell)

    return row


def read_csv(path: str) -> list[dict[str, str]]:
    """
    Reads and parses a CSV file.

    Args:
        path (str): The path of the CSV file.

    Returns:
        (list[dict[str, str]]): A list of rows, which are each made up of header-value pairs.
    """
    lines: str = readall(path).splitlines()
    rows: list[list[str]] = [parse_csv_line(line) for line in lines]

    entries: list[dict[str, str]] = []
    for row in rows[1:]:
        entry: dict[str, str] = {}
        for header, data in zip(rows[0], row):  # First row is column headers
            entry[header] = data

        entries.append(entry)

    return entries


def get_by_country_code(data: list[dict[str, str]], code: str) -> dict[str, str] | None:
    """
    Gets a country from the data set by country code.

    Args:
        data (list[dict[str, str]]): The data set.
        code (str): The country code to search for.

    Returns:
        (dict[str, str] | None): The country, if one could be found, else None.
    """
    for country in data:
        if "Country Code" in country and country["Country Code"] == code:
            return country

    return None


def get_masked(xs: list[int], ys: list[float | None]) -> tuple[list[int], list[float]]:
    """
    Gets a masked version of the data.

    Args:
        xs (list[int]): The list of data points along the x axis.
        ys (list[float | None]): The list of data points along the y axis.

    Returns:
        (tuple[list[int], list[float]]): The list of data points, masked by whether the y value was None.
    """

    xmasked: list[int] = []
    ymasked: list[float] = []

    for x, y in zip(xs, ys):
        if y is not None:
            xmasked.append(x)
            ymasked.append(y)

    return (xmasked, ymasked)


def plot(country1: dict[str, str], country2: dict[str, str], label: str) -> None:
    """
    Plots a graph of 2 countries' data.

    Args:
        country1 (dict[str, str]): The first country.
        country2 (dict[str, str]): The second country.
        label (str): The y axis label.
    """

    series1 = get_series(country1)
    series2 = get_series(country2)

    (s1decades, s1masked) = get_masked(get_decades(), series1)
    (s2decades, s2masked) = get_masked(get_decades(), series2)

    plt.plot(s1decades, s1masked, label=country1["Country Name"])
    plt.plot(s2decades, s2masked, label=country2["Country Name"])

    plt.legend(loc="upper left")

    plt.xlabel("Year")
    plt.ylabel(label)

    plt.axis((1960, 2030, min(*s1masked, *s2masked), max(*s1masked, *s2masked)))

    plt.show()


def get_decade_percentage_increase(
    decade: int, country: dict[str, str]
) -> float | None:
    """
    Calculate the percentage increase for a specific decade.

    Args:
        decade (int): The decade to get the percentage increase in.
        country (dict[str, str]): The country to get the data from.

    Returns:
        (float | None): The percentage increase for the decade, or None if there was missing/invalid data.
    """

    try:
        before = float(country[str(decade - 9)])
        after = float(country[str(decade)])

        if before == 0:
            return None

        return ((after - before) / before) * 100
    except:
        return None


def get_decades() -> list[int]:
    """
    Gets the list of decades for the data range.

    Returns:
        list[int]: The list of decades.
    """
    return list(range(1970, 2030, 10))


def get_series(country: dict[str, str]) -> list[float | None]:
    """
    Gets the data series of percentage increases for a country.

    Args:
        country (dict[str, str]): The country to get the data for.

    Returns:
        (list[Float | None]): The data series of percentage increases for the specified country.
    """
    return [get_decade_percentage_increase(decade, country) for decade in get_decades()]


def to_string_or_empty(input: any) -> str:
    """
    Convert a value to a string, with None mapping to an empty string.

    Returns:
        str: The stringified input, with empty strings for None values.
    """
    if input is None:
        return ""
    return str(input)


def write_results(path: str, rows: list[list[any]]) -> None:
    """
    Write a table of results out to a file.

    Args:
        path (str): The path to the table of results file.
        rows (list[list[any]]): The list of rows to write to the table of results file.
    """
    writeall(path, "\n".join([",".join(map(to_string_or_empty, row)) for row in rows]))


def main() -> None:
    """
    Loads both data sets, gets the user to select a country, and then produces graphs and table of results.
    """
    populations = read_csv("data/World Population data 2024.csv")
    life_expectancies = read_csv("data/World Life Expectancy.csv")

    uk_population = get_by_country_code(populations, "GBR")
    uk_life_expectany = get_by_country_code(life_expectancies, "GBR")
    if uk_population is None or uk_life_expectany is None:
        print("Can't find UK")
        return

    selected_population = None
    selected_life_expectancy = None
    while selected_population is None or selected_life_expectancy is None:
        code = input("Enter country code: ").upper()
        selected_population = get_by_country_code(populations, code)
        selected_life_expectancy = get_by_country_code(life_expectancies, code)
        if None in (selected_population, selected_life_expectancy):
            print("Sorry, there is no such country in the data")
            continue

        population_samples = [
            data for data in get_series(selected_population) if data is not None
        ]
        life_expectancy_samples = [
            data for data in get_series(selected_life_expectancy) if data is not None
        ]

        if len(population_samples) == 0 or len(life_expectancy_samples) == 0:
            print("Sorry there is no data for this country")
            selected_population = None
            selected_life_expectancy = None

    write_results(
        "population_results.csv",
        [get_decades(), get_series(uk_population), get_series(selected_population)],
    )

    plot(
        uk_population,
        selected_population,
        "Population (% inc.)",
    )

    write_results(
        "life_expectancy_results.csv",
        [
            get_decades(),
            get_series(uk_life_expectany),
            get_series(selected_life_expectancy),
        ],
    )

    plot(
        uk_life_expectany,
        selected_life_expectancy,
        "Life Expectancy (% inc.)",
    )


if __name__ == "__main__":
    main()
