"""
    create grid_proxy:
        Retrieves the grid certificate proxy from the users certificate.
        
    Usage:
        create grid_proxy [vo=<x>] [hours=<x>]
        
    Parameters:
        vo:    Virtual Organisation (VO) to assign.
               User must be member of that VO.
               Default: cms
        hours: Number of hours the proxy should be valid for.
               Default: 80. Must be an integer. The maximum allowed
               length depends on the machine configuration.
              
"""
import logging
from .. import Command as C

LOG = logging.getLogger(__name__)


class Command(C):

    DEFAULTS = {
        'vo': 'cms',
        'hours': 80,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        from ntp.interpreter import call
        vo = self.__variables['vo']
        hours = str(self.__variables['hours'])
        command = ['voms-proxy-init', '-voms', vo, '-hours', hours]
        call(
            ' '.join(command),
            logger=LOG,
            shell=True,
        )

        return True
