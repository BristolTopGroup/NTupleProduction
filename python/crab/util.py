import os
import sys
from .das_client import get_data
from .datasets import create_sample_list
import json
import logging

LOG = logging.getLogger(__name__)

NTPROOT = os.environ['NTPROOT']
CACHE = NTPROOT + '/workspace/cache'
CRAB_CFG_PATH = NTPROOT + '/python/crab'


def get_dataset(campaign, dataset_alias):
    samples = create_sample_list()
    if not campaign in samples:
        raise KeyError("Campaign '{0}' is not known!".format(campaign))
    if not dataset_alias in samples[campaign]:
        raise KeyError(
            "Dataset alias '{0}' is not known!".format(dataset_alias))
    return samples[campaign][dataset_alias]


def ask_das(query):
    host = 'https://cmsweb.cern.ch'
    LOG.info('Querying DAS ({0}): "{1}"'.format(host, query))
    idx = 0
    limit = 0
    debug = False
    data = get_data(host, query, idx, limit, debug)
    if isinstance(data, basestring):
        dasjson = json.loads(data)
    else:
        dasjson = data
    status = dasjson.get('status')
    if status == 'ok':
        data = dasjson.get('data')
        return data


def drop_das_fields(row):
    """Drop DAS specific headers in given row"""
    LOG.debug("Removing DAS fields")
    for key in ['das', 'das_id', 'cache_id', 'qhash']:
        if row.has_key(key):
            del row[key]


def get_files(campaign, dataset_alias):
    LOG.info("Searching for files of {0}/{1}".format(campaign, dataset_alias))
    files = []
    dataset = get_dataset(campaign, dataset_alias)
    query = "file dataset={0}".format(dataset)
    data = ask_das(query)
    for row in data:
        drop_das_fields(row)
        if 'file' in row:
            f = row['file'][0]['name']
            files.append(f)
    # TODO: cache the response
    LOG.info("Found {0} files".format(len(files)))
    return files


def find_input_files(campaign, dataset, variables, logger):
    input_files = []
    if variables['files'] != "":
        input_files = variables['files'].split(',')
    if input_files:
        logger.debug(
            'Chosen input files:\n{0}'.format('  \n'.join(input_files)))
    else:
        input_files = get_files(campaign, dataset)

    def __check_files(input_files):
        exists = []
        for f in input_files:
            if not f.startswith('/store') and not 'file://' in f:
                if not os.path.exists(f):
                    logger.error('Could not find file "{0}"!'.format(f))
                    exists.append(False)
                    continue
            exists.append(True)
        return all(exists)

    def __fix_paths(input_files):
        new_paths = []
        for f in input_files:
            if not f.startswith('/store') and not 'file://' in f:
                f = 'file://' + os.path.abspath(f)
            new_paths.append(f)
        return new_paths

    if not __check_files(input_files):
        sys.exit(-1)

    input_files = __fix_paths(input_files)

    return input_files


def get_user():
    from CRABClient.UserUtilities import getUsernameFromSiteDB, UsernameException

    LOG = logging.getLogger(__name__)
    user = 'nobody'
    try:
        user = getUsernameFromSiteDB()
    except UsernameException, e:
        import traceback
        LOG.error(
            'Could not get user name from https://cmsweb.cern.ch/sitedb/data/prod/whoami')
        LOG.error(traceback.format_exc(e))
        import getpass
        user = getpass.getuser()
#         LOG.info('Guessing user from cert')
#         import subprocess
#         p = subprocess.Popen('voms-proxy-info -identity', stdout = subprocess.PIPE, shell = True)
#         result, _ = p.communicate()
#         USER = result.split(' ')[-1]
#         LOG.info('Found {0}'.format(USER))
    return user
