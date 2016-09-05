"""
    A small collections of functions that are useful in more than one place.
    All of this should move to DailyPythonScripts.
"""
from __future__ import division


def make_even_chunks(list_of_things, size_of_chunk):
    """
        Creates even chunks given a list and the number of chunks.
        @param: list_of_things: the list to be chunked
        @param: size_of_chunk: the minimal size of a chunk.
        This method will re-distribute items if the last chunk is smaller than
        size_of_chunks.
        E.g. list_of_things = list(range(100)) and size_of_chunk = 9
        will give you 10 groups where one of them has 10 and all others have 9.
    """
    n_items = len(list_of_things)
    size_of_chunk = min(size_of_chunk, n_items)
    n = size_of_chunk
    n_groups = int(n_items / n)

    last = 0
    for i in range(1, n_groups + 1):
        cur = int(round(i * n_items / n_groups))
        yield list_of_things[last:cur]
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


def read(*names, **kwargs):
    import io, os
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_path):
    import re
    version_file = read(*file_path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
