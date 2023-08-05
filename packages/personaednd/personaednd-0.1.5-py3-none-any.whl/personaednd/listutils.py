from random import choice


def merge(original: list, values: list):
    for value in values:
        if value in original:
            original.remove(value)
        else:
            original.append(value)
    return original


def pick(iterable: list):
    selection = choice(iterable)
    iterable.remove(selection)
    return selection


def purge(original: list, purged_values: list):
    for value in purged_values:
        if value in original:
            original.remove(value)
    return original
