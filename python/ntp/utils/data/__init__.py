"""
    A collection of functions that operate on data
"""
import numpy as np

def is_real_data(file_path):
    """
        Tries to determine from the file path if the file is real data or
        simulation.
    """
    real_data_examples = [
        'SingleElectron', 'SingleMuon', 'ElectronHad', 'SingleMu']

    return any([e in file_path for e in real_data_examples])


def is_ttbar_mc(file_path):
    ttbar_mc_examples = ['TTJets', 'TTZ', 'TT_']
    return any([e in file_path for e in ttbar_mc_examples])


def good_object_filter(row, columns):
    channel = row['channel']
    goodJetIndex = []
    signalElectrons = row[
        'TopPairElectronPlusJetsSelection.signalElectronIndices']
    signalMuons = row['TopPairMuonPlusJetsSelection.signalMuonIndices']
    if channel == 'electron':
        goodJetIndex = row['TopPairElectronPlusJetsSelection.cleanedJetIndex']
    if channel == 'muon':
        goodJetIndex = row['TopPairMuonPlusJetsSelection.cleanedJetIndex']
    for column in columns:
        if column.startswith('Electrons.'):
            row[column] = [row[column][i] for i in signalElectrons]
        if column.startswith('Muons.'):
            row[column] = [row[column][i] for i in signalMuons]
        if column.startswith('Jets.'):
            row[column] = [row[column][i] for i in goodJetIndex]
    return row


def fix_lists(s):
    if type(s) is str:
        if '[' in s or '(' in s:
            tmp = s[1:-1]
            l = tmp.split()
            try:
                l = [int(i) for i in l]
            except ValueError:
                try:
                    l = [float(i) for i in l]
                except ValueError:
                    try:
                        l = [bool(i) for i in l]
                    except ValueError:
                        pass
            return l
    elif type(s) is np.ndarray:
        return list(s)

    return s