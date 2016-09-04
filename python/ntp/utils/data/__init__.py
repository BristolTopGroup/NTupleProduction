"""
    A collection of functions that operate on data
"""


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
