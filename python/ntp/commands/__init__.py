import os
import pwd
import subprocess
import logging
import copy

LOG = logging.getLogger(__name__)


class Command(object):
    """Base class for all commands"""
    REQUIRE_GRID_CERT = False
    DEFAULTS = {}

    def __init__(self, path=__file__, doc=__doc__):
        current_path = os.path.split(path)[0]
        parent_folder = current_path.split("/")[-1]
        if parent_folder == 'commands':
            self.__name = 'ntp'
        else:
            self.__name = parent_folder
        self.__doc = doc
        self.__text = ''
        self.__variables = copy.deepcopy(self.DEFAULTS)

    def __can_run(self):
        return True

    def run(self, args, variables):
        """
            Runs the commands and an exit code (True if everything went OK)
        """
        self.__prepare(args, variables)
        self.__text = "NOT IMPLEMENTED"

        return True

    def help(self):
        """Returns a little help text with the description of the command."""
        if self.__doc:
            return self.__doc
        else:
            return 'Documentation for command "{0}" is missing'.format(self.__name)

    def parse_arguments(self, name, argv):
        pass

    def get_text(self):
        return self.__text

    def __set_variables(self, variables):
        """
            Overwrites defaults with set variables
        """
        for name, value in variables.items():
            if name in variables:
                self.__variables[name] = value

    def __prepare(self, args, variables):
        self.__set_variables(variables)
        if self.REQUIRE_GRID_CERT:
            proxy = '/tmp/x509up_u{0}'.format(pwd.getpwuid(os.getuid()).pw_uid)
            if not self.__has_valid_proxy(proxy):
                subprocess.call(
                    ['voms-proxy-init', '-voms', 'cms'], shell=True)

    def __has_valid_proxy(self, proxy):
        from ntp.interpreter import call
        is_valid = os.path.isfile(proxy)
        if is_valid:
            _, stdout, _ = call(
                'voms-proxy-info --timeleft', logger=LOG, shell=True)
            time_left = int(stdout)
            LOG.info('Time left on proxy: {0} min'.format(time_left / 60))
            if time_left < (60 * 30):  # less than 30min
                is_valid = False
        return is_valid
