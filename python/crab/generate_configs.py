BASE = """
from crab.base import config
NAME = __file__.split('/')[-1]
NAME = NAME.replace('.py', '')

config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.inputDataset = '{dataset}'
config.Data.splitting = '{splitting}'
config.Data.unitsPerJob = {unitsPerJob}
config.Data.outLFNDirBase += '/{campaign}'
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
    }

    for campaign, samples in DATASETS.items():
        path = CRAB_CFG_PATH + '/' + campaign
        if not os.path.exists(path):
            os.mkdir(path)

        for alias, dataset in samples.items():
            unitsPerJob = 10
            splitting = 'FileBased'
            extras = ''

            file_path = path + '/' + alias + '.py'
            if 'TTJets' in alias or 'TT_' in alias:
                unitsPerJob = 5
                extras = "config.JobType.pyCfgParams = ['isTTbarMC=1']"
            if not 'MINIAODSIM' in dataset:
                # data
                unitsPerJob = 500000
                splitting = 'EventAwareLumiBased'
                if campaign in LUMI_MASKS:
                    extras = "config.Data.lumiMask = '{0}'".format(
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
