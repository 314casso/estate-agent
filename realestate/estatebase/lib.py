def first_last(iterable):
    i = iter(iterable)
    f = next(i)
    yield f, "first"
    n = next(i)
    for another in i:
        yield n, None
        n = another
    yield n, "last"
