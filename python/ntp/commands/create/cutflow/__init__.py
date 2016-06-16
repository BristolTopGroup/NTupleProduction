"""
    cutflow:
        Lists the cut-flow for a given ntuple file. Can produce either a
        summary (default) or a detailed list of events.
        
    Usage:
        cutflow ntuple.root [format=table,JSON]
        
    Parameters:
        format: The format of the output. Default: table
"""
from __future__ import division
import logging
import os
from .. import Command as C
from ntp.commands.setup import RESULTDIR

LOG = logging.getLogger(__name__)

MUON_CHANNEL = 'topPairMuPlusJetsSelectionAnalyser/consecutiveCuts'
ELECTRON_CHANNEL = 'topPairEPlusJetsSelectionAnalyser/consecutiveCuts'

# TODO load CMSSW into PYTHONPATH


class Command(C):

    DEFAULTS = {
        'format': 'table',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        input_file = args[0]
        LOG.debug('Reading {0}'.format(input_file))

        output_format = self.__variables['format']
        if output_format.lower() == 'table':
            self.__create_table(input_file)
        elif output_format.lower() == 'json':
            self.__create_full_json(input_file)
        else:
            self.__text = 'Unknown format "{0}"'.format(output_format)
            return False
        return True

    def __create_table(self, input_file):
        from ROOT import TFile
        f = TFile.Open(input_file)
        mu_hist = f.Get(MUON_CHANNEL)
        e_hist = f.Get(ELECTRON_CHANNEL)

        mu_cutflow = self.__extract_numbers_and_labels(mu_hist)
        e_cutflow = self.__extract_numbers_and_labels(e_hist)

        f.Close()

        self.__text = "Cutflow for muon channel:\n"
        self.__format_cutflow(mu_cutflow)
        self.__text += "\nCutflow for electron channel:\n"
        self.__format_cutflow(e_cutflow)

    def __extract_numbers_and_labels(self, histogram):
        n_bins = histogram.GetNbinsX()
        cutflow = []
        for i in range(1, n_bins + 1):
            name = histogram.GetXaxis().GetBinLabel(i)
            value = int(histogram.GetBinContent(i))
            cutflow.append((name, value))
        return cutflow

    def __format_cutflow(self, cutflow):
        headers = ['Step #', 'Step name', '# events', 'eff', 'total eff']
        max_len_name = max([len(name) for (name, _) in cutflow])
        # add some space
        row_format = "{:<3}\t"
        row_format += "{:<" + str(max_len_name) + "}\t"
        row_format += "{:<10}\t"
        row_format += "{:<3}%\t"
        row_format += "{:<3}%\n"

        self.__text += row_format.format(*headers)
        self.__text += '-' * (30 + max_len_name)
        self.__text += '\n'

        for i, c in enumerate(cutflow):
            name, value = c
            total_efficiency = round(value / cutflow[0][1] * 100., 2)
            efficiency = 100.
            if i > 0:
                efficiency = round(value / cutflow[i - 1][1] * 100., 2)
            outputs = [i, name, value, efficiency, total_efficiency]
            self.__text += row_format.format(*outputs)

    def __create_full_json(self, input_file):
        from ROOT import TFile
        e_prefix = 'TopPairElectronPlusJetsSelection'
        mu_prefix = 'TopPairMuonPlusJetsSelection'
        e_steps = [
            'AllEvents',
            'EventCleaningAndTrigger',
            'ExactlyOneSignalElectron',
            'LooseMuonVeto',
            'LooseElectronVeto',
            'ConversionVeto',
            'AtLeastOneGoodJet',
            'AtLeastTwoGoodJets',
            'AtLeastThreeGoodJets',
            'AtLeastFourGoodJets',
            'AtLeastOneBtag',
            'AtLeastTwoBtags',
        ]
        mu_steps = [
            'AllEvents',
            'EventCleaningAndTrigger',
            'ExactlyOneSignalMuon',
            'LooseMuonVeto',
            'LooseElectronVeto',
            'AtLeastOneGoodJet',
            'AtLeastTwoGoodJets',
            'AtLeastThreeGoodJets',
            'AtLeastFourGoodJets',
            'AtLeastOneBtag',
            'AtLeastTwoBtags',
        ]
        e_branches = [e_prefix + '.' + step for step in e_steps]
        mu_branches = [mu_prefix + '.' + step for step in mu_steps]
        f = TFile.Open(input_file)
        tree = f.Get('nTupleTree/tree')
        e_cutflow = {step:{} for step in e_steps}
        mu_cutflow = {step:{} for step in mu_steps}

        for event in tree:
            for step, branch in zip(e_steps, e_branches):
                self.__fill_cutflow(
                    e_cutflow[step], event, step, branch)
            for step, branch in zip(mu_steps, mu_branches):
                self.__fill_cutflow(
                    mu_cutflow[step], event, step, branch)
        f.Close()

        import json
        e_output = os.path.join(RESULTDIR, 'e_cutflow.json')
        mu_output = os.path.join(RESULTDIR, 'mu_cutflow.json')
        with open(e_output, 'w+') as f:
            f.write(json.dumps(e_cutflow))
        with open(mu_output, 'w+') as f:
            f.write(json.dumps(mu_cutflow))

    def __fill_cutflow(self, cutflow, event, step, branch):
        '''
            A cutflow dictionary sho8uld be of the form
            {
                "name": "name of step",
                "passing": {
                    run_number:{
                        lumi_section: [event_number, ...]
                    }
                }
            }
        '''
        run_number = 1
        lumi_section = 2
        event_number = 3
        passing = getattr(event, branch)
        if not passing:
            return

        if not "passing" in cutflow:
            cutflow["passing"] = {}

        if not run_number in cutflow["passing"]:
            cutflow["passing"][run_number] = {}

        if not lumi_section in cutflow["passing"][run_number]:
            cutflow["passing"][run_number][lumi_section] = []
        cutflow["passing"][run_number][lumi_section].append(event_number)
