from matplotlib import pyplot as plt


def plot(
    decade: list[int], series1: list[float], series2: list[float], label: str
) -> None:
    plt.plot(decade, series1)
    plt.plot(decade, series2)

    plt.xlabel("Year")
    plt.ylabel(label)

    plt.axis((1960, 2030, min(*series1, *series2), max(*series1, *series2)))

    plt.show()


if __name__ == "__main__":
    x = [1965, 1975, 1985, 1995, 2005, 2015, 2025]
    y = [5, 12, 19, 21, 31, 27, 35]
    z = [3, 5, 11, 20, 15, 29, 31]
    ylabel = "Life Expectancy"
    plot(x, y, z, ylabel)
