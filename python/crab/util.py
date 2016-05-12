import os
from .das_client import get_data
from .datasets import create_sample_list
import json

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
    for key in ['das', 'das_id', 'cache_id', 'qhash']:
        if row.has_key(key):
            del row[key]


def get_files(campaign, dataset_alias):
    files = []
    dataset = get_dataset(campaign, dataset_alias)
    query = "file dataset={0}".format(dataset)
    data = ask_das(query)
    for row in data:
        drop_das_fields(row)
        if 'file' in row:
            file = row['file'][0]['name']
            files.append(file)
    # TODO: cache the response
    return files
