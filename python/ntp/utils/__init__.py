"""
    A small collections of functions that are useful in more than one place.
    All of this should move to DailyPythonScripts.
"""


def make_even_chunks(list_of_things, n_chunks):
    """
        Creates even chunks given a list and the number of chunks
    """
    last = 0
    n = n_chunks
    l = list_of_things
    for i in range(1, n + 1):
        cur = int(round(i * (len(l) / n)))
        yield l[last:cur]
        last = cur


def find_latest_iteration(directories):
    """
        Selects the latest iteration of a workflow based on the numbering
        of directories.
        Expects a list of directories of the form
        <path>/<name>_<number>
        and will return the directory with the highest number.
        Will return 0 if no directories are given.
    """
    numbers = [0]
    for d in directories:
        number = int(d.split('_')[-1])
        numbers.append(number)
    return max(numbers)
