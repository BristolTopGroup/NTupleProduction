"""
    cutflow:
        Lists the cut-flow for a given ntuple file. Can produce either a
        summary (default) or a detailed list of events passing each cut in
        JSON format. The JSON files can be later used for filtering.
        
    Usage:
        cutflow ntuple.root [format=table,JSON] [prefix=""]
        
    Parameters:
        format: The format of the output. Format=table will print a table on
                the screen while format=JSON will create two JSON files in 
                workspace/results with detailed information about which event
                passed which cut.
                Default: format=table
        prefix: prefix to use for resulting output files (e.g. if format=JSON)
"""
import logging
import os
from .. import Command as C
from ntp.commands.setup import CMSSW_SRC
from ntp.interpreter import time_function

LOG = logging.getLogger(__name__)
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Command(C):

    DEFAULTS = {
        'format': 'table',
        'prefix': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('create cutflow', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        input_file = args[0]
        LOG.debug('Reading {0}'.format(input_file))

        output_format = self.__variables['format']
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'python {CURRENT_FOLDER}/{script}.py {input_file} {args}',
        ]
        script = 'create_table'
        if output_format.lower() == 'table':
            script = 'create_table'
        elif output_format.lower() == 'json':
            script = 'create_json'
        else:
            self.__text = 'Unknown format "{0}"'.format(output_format)
            return False

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            CURRENT_FOLDER=CURRENT_FOLDER,
            input_file=input_file,
            script=script,
            args = self.__variables['prefix'],
        )

        from ntp.interpreter import call
        code, stdout, stderr = call(
            [all_in_one], LOG, stdout_log_level=logging.DEBUG, shell=True)

        if not code == 0:
            LOG.error('An error occured: ' + stdout + stderr)
            return False
        
        self.__text = ''
        if output_format == 'table':
            import json
            output = self.__clean_stdout(stdout)
            text = json.loads(output)
            self.__text = '\n'.join(text)
        else:
            text = stdout
        return True
    
    def __clean_stdout(self, stdout):
        import re
        regex = '(\[")(.*?)("\])'
        m = re.search(regex, stdout)
        result = stdout
        if m:
            # 1st group == ["
            # 2nd group json
            # 3rd group == "]
            result =  m.group(1) + m.group(2) +  m.group(3)
            return result
        return result