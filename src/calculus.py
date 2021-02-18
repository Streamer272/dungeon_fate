import math


def test() -> any:
    #      c
    # A _______ B
    #  \       |
    #   \      |
    #    \     |
    #     \    |
    #    b \   | a
    #       \  |
    #        \ |
    #         \|
    #          C
    c = 3
    a = 4
    b = 5

    print("Ratio: " + str(b / a))

    # f = coordinate we want to find
    f_x = (a / b) * (2 * (b / a))
    f_y = (c / b) * (2 * (b / a))
    f_d = 2 * (b / a)

    print("F_D: " + str(f_d))
    print("F x: " + str(f_x))
    print("F y: " + str(f_y))


if __name__ == '__main__':
    test()
