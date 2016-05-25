"""
    list triggers:    lists all HLT triggers for a file

        Usage:
            list triggers <path to ROOT file>
"""
import logging
import os
from .. import Command as C
from ntp.commands.setup import CMSSW_SRC
from ntp.interpreter import time_function

LOG = logging.getLogger(__name__)
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
XROOTD_SERVER = 'xrootd-cms.infn.it'
IDENTIFIER = '=============='

class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('list triggers', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        input_file = args[0]
        if not input_file.startswith('/store'):
            input_file = os.path.abspath(input_file)
        else:
            if not self.__has_valid_proxy():
                self.__create_proxy()
            input_file = 'root://{XROOTD_SERVER}/{input_file}'.format(
                XROOTD_SERVER=XROOTD_SERVER,
                input_file=input_file
            )
        self.__input_file = input_file
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'python {CURRENT_FOLDER}/run.py {input_file}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            CURRENT_FOLDER=CURRENT_FOLDER,
            input_file=input_file
        )

        from ntp.interpreter import call
        code, stdout, stderr = call(
            [all_in_one], LOG, stdout_log_level=logging.DEBUG, shell=True)

        if code == 0:
            self.__extract_triggers(stdout, stderr)
        else:
            LOG.error('An error occured: ' + stderr)
            return False

        return True

    def __extract_triggers(self, stdout, stderr):
        import json
        stdout = self.__clean_stdout(stdout)
        result = {}
        try:
            result = json.loads(stdout)
        except ValueError:
            import traceback
            LOG.error('Could not read triggers')
            LOG.error(traceback.format_exc())
            

        if result:
            triggers = result['triggers']
            self.__text = 'Found {0} triggers in file {1}:\n'.format(
                len(triggers), self.__input_file)
            self.__print_triggers(triggers)
        else:
            LOG.error('An error occured: ' + stderr)
            
    def __clean_stdout(self, stdout):
        import re
        regex = '({0})(.*?)({0})'.format(IDENTIFIER)
        m = re.search(regex, stdout)
        result = stdout
        if m:
            # 1st group == IDENTIFIER
            # 2nd group json
            # 3rd group == IDENTIFIER
            result = m.group(2)
            return result
        return result
        

    def __print_triggers(self, triggers):
        for t in triggers:
            self.__text += '\t{name}, prescale={prescale}\n'.format(**t)
