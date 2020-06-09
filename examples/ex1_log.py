import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.rcdefaults()                # remove custom styles
params = {"svg.fonttype": "none"}  # try to use system font in svg


def main():
    x = np.logspace(-3, 3)
    y = x ** 2
    plt.figure()
    plt.plot(x, y, label="$y = x^{2}$")
    plt.xlabel("Some text of x")
    plt.ylabel("Some math text $y = x^{2}$")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.savefig("img/ex1-log.svg")


if __name__ == "__main__":
    main()
