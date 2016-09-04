"""
    run grid:    Uses CRAB3 to submit jobs to the WLCG grid
        Usage:
            run grid [campaign=<X>]  [dataset=<X>] [skip=<X>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in python/crab/*
            dataset:  Alias for the dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is to run over all datasets for a given campaign.
            skip:     Alias for datasets you want to skip.
                      Accepts wild-cards and comma-separated lists.
"""

from __future__ import print_function
import logging
import os
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC

from .. import Command as C


LOG = logging.getLogger(__name__)
CONFIG_PATH = '{NTPROOT}/python/crab/{campaign}/{dataset}.py'


class Command(C):

    DEFAULTS = {
        'campaign': 'Spring16',
        'dataset': 'TTJets_PowhegPythia8',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        campaign = self.__variables['campaign']
        dataset = self.__variables['dataset']

        from hepshell.interpreter import call
        crab_config = CONFIG_PATH.format(
            NTPROOT=NTPROOT,
            campaign=campaign,
            dataset=dataset,
        )
        if not os.path.exists(crab_config):
            LOG.error(
                'Requested config file ({0}) does not exist!'.format(crab_config))
            return False

        LOG.info('Submitting config file {0} to the grid'.format(crab_config))

        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'crab submit {crab_config}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            crab_config=crab_config
        )
        code, stdout, stderr = call(all_in_one, logger=LOG)

        return True
