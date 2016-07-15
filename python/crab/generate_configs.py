BASE = """import crab.base
from copy import deepcopy
NAME = __file__.split('/')[-1].replace('.pyc', '')
NAME = NAME.split('/')[-1].replace('.py', '')
CAMPAIGN = __file__.split('/')[-2]

config = deepcopy(crab.base.config)
config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.outLFNDirBase += '/' + CAMPAIGN
config.Data.inputDataset = '{dataset}'
config.Data.splitting = '{splitting}'
config.Data.unitsPerJob = {unitsPerJob}
{extras}

"""


def generate_crab_configs():
    from crab.datasets import DATASETS
    import os

    NTPROOT = os.environ['NTPROOT']
    CRAB_CFG_PATH = NTPROOT + '/python/crab'
    LUMI_MASKS = {
        '25ns': 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/' +
        'CAF/certification/Collisions15/13TeV/' +
        'Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt',
        'FALL15': '/hdfs/TopQuarkGroup/run2/json/ReReco_MinusBeamSpotIssue.txt',
        'Spring16' : 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/' +
        'CAF/certification/Collisions16/13TeV/' +
        'Cert_271036-275783_13TeV_PromptReco_Collisions16_JSON.txt',
    }

    for campaign, samples in DATASETS.items():
        path = CRAB_CFG_PATH + '/' + campaign

        if not os.path.exists(path):
            os.mkdir(path)

        for alias, dataset in samples.items():

            isReHLT = False
            if 'reHLT' in dataset: isReHLT = True

            unitsPerJob = 10
            splitting = 'FileBased'
            extras = ''

            file_path = path + '/' + alias + '.py'
            if 'TTJets' in alias or 'TT_' in alias:
                unitsPerJob = 5
                extras += "config.JobType.pyCfgParams = ['isTTbarMC=1']"
            if isReHLT:
                if extras:
                    extras = extras.replace(']','')
                    extras += ",'isReHLT=1']\n"
                else:
                    extras += "config.JobType.pyCfgParams = ['isReHLT=1']\n"
            if not 'MINIAODSIM' in dataset:
                # data
                unitsPerJob = 500000
                splitting = 'EventAwareLumiBased'
                extras = "config.JobType.pyCfgParams = ['isData=1']"
                if campaign in LUMI_MASKS:
                    extras += "\nconfig.Data.lumiMask = '{0}'".format(
                        LUMI_MASKS[campaign])

            with open(file_path, 'w+') as f:
                content = BASE.format(
                    unitsPerJob=unitsPerJob,
                    splitting=splitting,
                    dataset=dataset,
                    campaign=campaign,
                    extras=extras,
                )
                f.write(content)

if __name__ == '__main__':
    generate_crab_configs()
