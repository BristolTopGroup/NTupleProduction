"""
    check grid_proxy:
        Retrieves the grid certificate proxy from the users certificate.
        
    Usage:
        check grid_proxy
"""
import logging
import os
from .. import Command as C
from crab import das_client

LOG = logging.getLogger(__name__)


class Command(C):

    DEFAULTS = {
        'vo': 'cms',
        'hours': 80,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        self.__results = {
            'timeleft_in_seconds': 0,
            'timeleft_in_minutes': 0,
        }

    def run(self, args, variables):
        self.__prepare(args, variables)
        from ntp.interpreter import call
        proxy = das_client.x509()
        is_valid = os.path.isfile(proxy)
        time_left = 0

        if is_valid:
            _, stdout, stderr = call(
                'voms-proxy-info --timeleft',
                logger=LOG,
                shell=True)
            raw_output = stdout if not stdout == '' else stderr
            try:
                time_left = int(raw_output)
            except:
                time_left = 0
                msg = 'Proxy exists ({0}) but '.format(proxy)
                msg + 'could not read time left on proxy.'
                LOG.warning(msg)
                LOG.debug(
                    "Command output: {0}".format(stdout.encode('string-escape')))
            self.__results['timeleft_in_seconds'] = time_left
            self.__results['timeleft_in_minutes'] = time_left / 60
            LOG.info('Time left on proxy: {0} min'.format(
                self.__results['timeleft_in_minutes']))
        else:
            LOG.error('Could not find proxy {0}'.format(proxy))

        return is_valid
