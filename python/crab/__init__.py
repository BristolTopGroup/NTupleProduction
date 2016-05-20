import os
import sys
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s [%(name)s]  %(levelname)s: %(message)s')
ch = logging.StreamHandler()
if not os.environ.get("DEBUG", False):
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
LOG.addHandler(ch)

try:
    import importlib
    import_module = importlib.import_module
except:
    import_module = __import__


def load_config(campaign, dataset):
    relative_path = 'crab.{campaign}.{dataset}'.format(
        campaign=campaign, dataset=dataset)
    LOG.debug('Trying to import {0}'.format(relative_path))
    print(relative_path)
    if sys.version_info < (2, 7):
        mod = import_module(relative_path, fromlist=['config'])
    else:
        mod = import_module(relative_path)
    if hasattr(mod, 'config'):
        return mod.config
    else:
        return None


def get_config(campaign, dataset):
    config_dict = {
        'requestName': '',
        'outputDatasetTag': '',
        'inputDataset': '',
        'splitting': 'FileBased',
        'unitsPerJob': 5,
        'outLFNDirBase': '',
        'lumiMask': '',
        'pyCfgParams': '',
    }
    config = load_config(campaign, dataset)

    if config:
        config_dict['requestName'] = config.General.requestName
        config_dict['outputDatasetTag'] = config.Data.outputDatasetTag
        config_dict['inputDataset'] = config.Data.inputDataset
        config_dict['splitting'] = config.Data.splitting
        config_dict['unitsPerJob'] = config.Data.unitsPerJob
        config_dict['outLFNDirBase'] = config.Data.outLFNDirBase
        if hasattr(config.Data, 'lumiMask'):
            config_dict['lumiMask'] = config.Data.lumiMask
        if hasattr(config.JobType, 'pyCfgParams'):
            config_dict['pyCfgParams'] = config.JobType.pyCfgParams
        return config_dict
    else:
        return {}
