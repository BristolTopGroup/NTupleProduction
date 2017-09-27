"""
    ntuple2pandas:
        Converts a flat ntuple (ROOT) into a Pandas DataFrame.
        Output is stored as 
    
    Usage:
        ntuple2pandas <root files> [--label=TTJet] [--output-dir=] \
                     [--branches=<json files with branches to save] \
                     [--summarise]
    
    Parameters:
        files: ntuple files to be used for input
        where:    Where to run the analysis. Can be 'local|DICE'.
                  Default is 'local'.
"""
import hepshell
from hepshell.interpreter import time_function
from crab.datasets import get_datasets


class Command(hepshell.Command):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'files': [],
        'noop': False,
        'where': 'local',
        'test': False,
    }

    def run(self, args, variables):
        self.__prepare(args, variables)
        campaign = self.__variables['campaign']
        dataset = self.__variables['dataset']
        datasets = get_datasets(
            campaign).keys() if dataset == 'all' else [dataset]
        results = []
        for dataset in datasets:
            results.append(self.__run(campaign, dataset))
        return all(results)

    def __run_payload(self):
        # TODO: add checking/dynamic subcommand discovery
        if self.__variables['where'] == 'local':
            from .local import Command as PayLoad
        else:
            from .DICE import Command as PayLoad

        payload = PayLoad()
        return payload.run(self.__args, self.__variables)