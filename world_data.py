from pprint import pprint
from matplotlib import pyplot as plt


def readall(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def writeall(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def parse_csv_line(line: str) -> list[str]:
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


def read_csv(path: str) -> dict[str, str]:
    lines: str = readall(path).splitlines()
    rows: list[list[str]] = [parse_csv_line(line) for line in lines]

    entries: list[dict[str, str]] = []
    for row in rows[1:]:
        entry: dict[str, str] = {}
        for header, data in zip(rows[0], row):
            entry[header] = data

        entries.append(entry)

    return entries


def get_by_country_code(data: list[dict[str, str]], code: str) -> dict[str, str] | None:
    for country in data:
        if "Country Code" in country and country["Country Code"] == code:
            return country

    return None


def get_masked(xs: list[int], ys: list[float]) -> tuple[list[int], list[float]]:
    xmasked: list[int] = []
    ymasked: list[float] = []

    for x, y in zip(xs, ys):
        if y is not None:
            xmasked.append(x)
            ymasked.append(y)

    return (xmasked, ymasked)


def plot(
    country1: dict[str, str], country2: dict[str, str], label: str
) -> None:
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
    try:
        before = float(country[str(decade - 9)])
        after = float(country[str(decade)])

        if before == 0:
            return None

        return ((after - before) / before) * 100
    except:
        return None

def get_decades() -> list[int]:
    return list(range(1970, 2030, 10))


def get_series(country: dict[str, str]) -> list[float | None]:
    return [get_decade_percentage_increase(decade, country) for decade in get_decades()]

def to_string_or_empty(input: any) -> str:
    if input is None:
        return ""
    return str(input)

def write_results(path: str, rows: list[list[any]]):
    writeall(path, "\n".join([",".join(map(to_string_or_empty, row)) for row in rows]))

def main():
    populations = read_csv("data/World Population data 2024.csv")
    life_expectancies = read_csv("data/World Life Expectancy.csv")
    uk_population = get_by_country_code(populations, "GBR")
    uk_life_expectany = get_by_country_code(life_expectancies, "GBR")
    if uk_population is None or uk_life_expectany is None:
        print("Can't find UK")
        return

    selected_population = None
    selected_life_expectancy = None
    code = None
    while selected_population is None or selected_life_expectancy is None:
        code = input("Enter country code: ").upper()
        selected_population = get_by_country_code(populations, code)
        selected_life_expectancy = get_by_country_code(life_expectancies, code)
        if None in (selected_population, selected_life_expectancy):
            print("Sorry, there is no such country in the data")
            continue

        if len([data for data in get_series(selected_population) + get_series(selected_life_expectancy) if data is not None]) == 0 :
            print("Sorry there is no data for this country")    
            country = None

    write_results("population_results.csv", [
        get_decades(),
        get_series(uk_population),
        get_series(selected_population)
    ])

    plot(
        uk_population,
        selected_population,
        "Population (% inc.)",
    )

    write_results("life_expectancy_results.csv", [
        get_decades(),
        get_series(uk_life_expectany),
        get_series(selected_life_expectancy)
    ])

    plot(
        uk_life_expectany,
        selected_life_expectancy,
        "Life Expectancy (% inc.)",
    )


if __name__ == "__main__":
    main()
