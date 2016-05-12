"""
    run grid:    Uses CRAB3 to submit jobs to the WLCG grid
        Usage:
            run grid [campaign=<X>]  [dataset=<X>] [skip=<X>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
            dataset:  Alias for the dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is to run over all datasets for a given campaign.
            skip:     Alias for datasets you want to skip.
                      Accepts wild-cards and comma-separated lists.
"""

from __future__ import print_function
from .. import Command as C


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "NOT IMPLEMENTED - but would be running on the grid"

        return True
