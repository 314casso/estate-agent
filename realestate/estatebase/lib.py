def expt(b, n):
    if n == 0:
        return 1
    return b * expt(b, n - 1)
