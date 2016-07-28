import logging
import sys
import ntp
LOG = logging.getLogger('ntp.commands.create.cutflow')

TREE_PATH = 'nTupleTree/tree'
E_PREFIX = 'TopPairElectronPlusJetsSelection'
MU_PREFIX = 'TopPairMuonPlusJetsSelection'
E_STEPS = [
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
MU_STEPS = [
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


def fill_cutflow(cutflow, event, step, branch):
    '''
        A cutflow dictionary sho8uld be of the form
        {
            "name of step": {
                "passing": {
                    run_number:{
                        lumi_section: [event_number, ...]
                    }
                }
            }
        }
    '''
    run_number = getattr(event, 'Event.Run')
    lumi_section = getattr(event, 'Event.LumiSection')
    event_number = getattr(event, 'Event.Number')
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


def read_cutflows(input_file):
    from ROOT import TFile

    LOG.debug('Reading {0}'.format(input_file))
    f = TFile.Open(input_file)
    tree = f.Get(TREE_PATH)

    e_branches = [E_PREFIX + '.' + step for step in E_STEPS]
    mu_branches = [MU_PREFIX + '.' + step for step in MU_STEPS]

    e_cutflow = {step: {} for step in E_STEPS}
    mu_cutflow = {step: {} for step in MU_STEPS}

    for event in tree:
        for step, branch in zip(E_STEPS, e_branches):
            fill_cutflow(e_cutflow[step], event, step, branch)

        for step, branch in zip(MU_STEPS, mu_branches):
            fill_cutflow(mu_cutflow[step], event, step, branch)
    f.Close()

    return e_cutflow, mu_cutflow


def write_json(e_cutflow, mu_cutflow, prefix):
    import json
    import os
    from ntp.commands.setup import RESULTDIR

    if not prefix == '' and not prefix.endswith('_'):
        prefix += '_'

    e_output = os.path.join(RESULTDIR, prefix + 'e_cutflow.json')
    mu_output = os.path.join(RESULTDIR, prefix + 'mu_cutflow.json')

    LOG.info('Creating electron cutflow file: {0}'.format(e_output))
    with open(e_output, 'w+') as f:
        f.write(json.dumps(e_cutflow, indent=4))

    LOG.info('Creating muon cutflow file: {0}'.format(mu_output))
    with open(mu_output, 'w+') as f:
        f.write(json.dumps(mu_cutflow, indent=4))

if __name__ == '__main__':
    LOG.debug('Creating JSON files with full event details')
    input_file = None
    prefix = ''
    n_args = len(sys.argv)
    if n_args > 1:
        input_file = sys.argv[1]
        if n_args == 3:
            prefix = str(sys.argv[2])
    else:
        LOG.error('No input file specified.')
        sys.exit(-1)

    e_cutflow, mu_cutflow = read_cutflows(input_file)

    write_json(e_cutflow, mu_cutflow, prefix)
