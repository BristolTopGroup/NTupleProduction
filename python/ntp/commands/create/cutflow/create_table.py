from __future__ import print_function, division
import logging
import sys
from ROOT import TFile
import ntp
LOG = logging.getLogger('ntp.commands.create.cutflow')


MUON_CHANNEL = 'topPairMuPlusJetsSelectionAnalyser/consecutiveCuts'
ELECTRON_CHANNEL = 'topPairEPlusJetsSelectionAnalyser/consecutiveCuts'


def extract_numbers_and_labels(histogram):
    n_bins = histogram.GetNbinsX()
    cutflow = []
    for i in range(1, n_bins + 1):
        name = histogram.GetXaxis().GetBinLabel(i)
        value = int(histogram.GetBinContent(i))
        cutflow.append((name, value))
    return cutflow


def format_cutflow(cutflow):
    headers = ['Step #', 'Step name', '# events', 'eff', 'total eff']
    max_len_name = max([len(name) for (name, _) in cutflow])
    # add some space
    row_format = "{:<3}\t"
    row_format += "{:<" + str(max_len_name) + "}\t"
    row_format += "{:<10}\t"
    row_format += "{:<3}%\t"
    row_format += "{:<3}%"

    header_format = row_format.replace('%', "")

    text = [header_format.format(*headers)]
    text.append('-' * (30 + max_len_name))
    text.append('')
    for i, c in enumerate(cutflow):
        name, value = c
        total_efficiency = round(value / cutflow[0][1] * 100., 2)
        efficiency = 100.
        if i > 0:
            efficiency = round(value / cutflow[i - 1][1] * 100., 2)
        outputs = [i, name, value, efficiency, total_efficiency]
        text.append(row_format.format(*outputs))
    return text

if __name__ == '__main__':
    LOG.debug('Creating cutflow table')
    input_file = None
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        LOG.error('No input file specified.')
        sys.exit(-1)
    LOG.debug('Reading {0}'.format(input_file))
    f = TFile.Open(input_file)
    mu_hist = f.Get(MUON_CHANNEL)
    e_hist = f.Get(ELECTRON_CHANNEL)

    mu_cutflow = extract_numbers_and_labels(mu_hist)
    e_cutflow = extract_numbers_and_labels(e_hist)

    f.Close()

    text = ["Cutflow for electron channel:"]
    text.extend(format_cutflow(e_cutflow))
    text.append('')
    text.append("Cutflow for muon channel:")
    text.extend(format_cutflow(mu_cutflow))
    import json
    print(json.dumps(text))
