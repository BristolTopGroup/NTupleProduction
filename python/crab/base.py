import os
import datetime
import logging
from WMCore.Configuration import Configuration
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI
from CRABClient.UserUtilities import getUsernameFromSiteDB, UsernameException
from crab.util import get_user
LOG = logging.getLogger(__name__)
USER = get_user()

# env variables
if not 'HEP_PROJECT_ROOT' in os.environ:
    import sys
    print('Cannot find HEP_PROJECT_ROOT env variable. Did you "source bin/env.sh"?')
    sys.exit(-1)

# this is the NTupleVersion!
__version__ = '1.0.5'
NTPROOT = os.environ['HEP_PROJECT_ROOT']
WORKSPACE = os.path.join(NTPROOT, 'workspace')
CRAB_WS = os.path.join(WORKSPACE, 'crab')
TODAY = datetime.date.today().isoformat()
PSET = NTPROOT + '/python/run/miniAODToNTuple_cfg.py'
INPUT_FILES = [
    'data/BTagSF/CSVv2_Moriond17_B_H.csv',
    'data/JEC/Spring16_25nsV6_DATA.db',
    'data/JEC/Spring16_25nsV6_MC.db',
]

config = Configuration()

config.section_("General")
config.General.requestName = 'TESTING'
config.General.workArea = 'workdirCrab/v{version}/{date}'.format(version=__version__, date=TODAY)
config.General.transferOutputs = True
# config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = PSET
config.JobType.allowUndistributedCMSSW = True
config.JobType.inputFiles = [NTPROOT + '/' + f for f in INPUT_FILES]

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/{user}/ntuple/v{version}'.format(
    user=USER, version=__version__)
config.Data.publication = True
# config.Data.ignoreLocality = True

config.section_("Site")
config.Site.storageSite = 'T2_UK_SGrid_Bristol'
config.Site.blacklist = ["T2_BR_SPRACE", "T2_UA_KIPT", "T2_BR_UERJ"]
