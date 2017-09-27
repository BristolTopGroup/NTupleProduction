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
"""

import hepshell
import pandas as pd
import root_numpy as rnp
import os
import numpy as np
import types

from ntp import NTPROOT
from ntp.commands.setup import RESULTDIR
from ntp.utils.data import good_object_filter, fix_lists
import logging
logger = logging.getLogger(__name__)


def split_column(df, column, maxEntries=-1, default_value=np.nan, index_column=None):
    class vgetter(object):

        def __init__(self, index=0, default_value=np.nan):
            self.__index = index
            self.__default_value = default_value

        def __call__(self, x):
            is_indexable = isinstance(x, types.ListType) or isinstance(
                x, types.TupleType) or type(x) is np.ndarray
            if not is_indexable:
                logger.warning('Not a list, returning {0}'.format(column))
                return x
            if len(x) > self.__index:
                return x[self.__index]
            else:
                return self.__default_value
    if maxEntries < 1:
        maxEntries = df[column].apply(len).max()
    for i in range(maxEntries):
        column_template = column + '[{0}]'
        if '.' in column:
            place = column.find('.')
            column_template = column[:place] + '[{0}]' + column[place:]
        df.loc[:, column_template.format(i)] = df[column].apply(
            vgetter(i, default_value))
    # remove old column
    del df[column]


def store_channels(df, output_file):
    df.rename(columns={
        'TopPairElectronPlusJetsSelection.FullSelection': 'passes_e_selection',
        'TopPairMuonPlusJetsSelection.FullSelection': 'passes_mu_selection',
    }, inplace=True)

    # masks for the two channels we are interested in
    electron_channel = df['passes_e_selection'] == 1
    muon_channel = df['passes_mu_selection'] == 1
    # add a few variables
    df.loc[electron_channel, 'channel'] = 'electron'
    df.loc[muon_channel, 'channel'] = 'muon'
    # only keep events that pass the electron or muon selection
    df = df[electron_channel | muon_channel]

    # some branches contain vectors of variables. We need to flatten them
    df.applymap(fix_lists)

    # split lists into individual columns
    should_flatten = lambda x: x.startswith(
        'Electrons.') or x.startswith('Muons.') or x.startswith('Jets.')
    columns_to_flatten = [c for c in df.columns if should_flatten(c)]
    # apply good object filter
    df = df.apply(good_object_filter, axis=1, columns=columns_to_flatten)

    # more variables
    df['nElectrons'] = df['Electrons.Pt'].apply(len)
    df['nMuons'] = df['Muons.Pt'].apply(len)
    df['nJets'] = df['Jets.Pt'].apply(len)
    max_electrons = df['nElectrons'].max()
    max_muons = df['nMuons'].max()
    max_jets = df['nJets'].max()

    for c in columns_to_flatten:
        maxEntries = -1
        if 'Jets.' in c:
            maxEntries = max_jets
        if 'Muons.' in c:
            maxEntries = max_muons
        if 'Electrons.' in c:
            maxEntries = max_electrons
        split_column(df, c, maxEntries=maxEntries, default_value=0)
    df.to_csv(output_file)


def get_branches(branches_json):
    import json
    with open(branches_json) as f:
        branches = json.load(f)
    # add auxiliary branches
    auxiliary_branches = [
        'TopPairElectronPlusJetsSelection.cleanedJetIndex',
        'TopPairElectronPlusJetsSelection.signalElectronIndices',
        'TopPairMuonPlusJetsSelection.cleanedJetIndex',
        'TopPairMuonPlusJetsSelection.signalMuonIndices',
    ]
    branches.extend(auxiliary_branches)
    return branches


class Command(hepshell.Command):
    DEFAULTS = {
        'tree': 'nTupleTree/tree',
        'branches': os.path.join(NTPROOT, 'data/pandas/branches.selected'),
        'output-dir': RESULTDIR,
        'summarise': True,
    }

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.output_files = []

        files = self.__args
        branches_json = self.__variables['columns']
        tree = self.__variables['tree']
        label = self.__variables['label']
        output_dir = self.__variables['output-dir']

        branches = get_branches(branches_json)

        for input_file in files:
            logger.info('Converting {0}'.format(input_file))
            data_root = rnp.root2array(
                input_file, treename=tree, branches=branches)
            df = pd.DataFrame(data_root, columns=branches)
            df.loc[:, 'label'] = label
            output_file = os.path.basename(input_file)
            output_file = input_file.replace('.root', '.csv')
            output_file = os.path.join(output_dir, output_file)
            store_channels(df, output_file)
            self.output_files.append(output_file)

        if len(self.output_files) > 1:
            summary = None
            for f in self.output_files:
                to_add = pd.read_csv(f)
                if summary is None:
                    summary = to_add
                else:
                    summary = summary.append(to_add, ignore_index=True)
                os.remove(f)
            summary_filename = 'summary_{0}.csv'.format(label)
            summary_filename = os.path.join(output_dir, summary_filename)
            summary.to_csv(summary_filename, index=False)

        return True


if __name__ == '__main__':
    variables = {
        'tree': 'nTupleTree/tree',
        'columns': os.path.join(NTPROOT, 'data/pandas/branches.selected'),
        'label': 'TTJet'
    }

    files = [os.path.join(RESULTDIR, 'TTJets_PowhegPythia8_Test_ntuple.root')]

    c = Command()
    c.run(files, variables)
