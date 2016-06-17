from __future__ import print_function
import readline
import string
import os
import shlex
import types
import sys
import logging
import select
import subprocess
import resource

LOG = logging.getLogger(__name__)

try:
    import importlib
    import_module = importlib.import_module
except:
    import_module = __import__

PROMPT = 'ntp > '
HISTFILE = os.path.expanduser('~/.ntp_history')
LOGFILE = os.path.expanduser('~/.ntp_log')
COMPLETEKEY = 'tab'

CURRENT_PATH = os.path.split(__file__)[0]
COMMAND_PATH = os.path.join(CURRENT_PATH, 'commands')

PATH_TO_BASE = os.path.join(CURRENT_PATH, '..')
BASE_MODULE = 'ntp.commands'


def time_function(name, logger):
    def _time_function(function):
        def __time_function(*args, **kwargs):
            usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
            result = function(*args, **kwargs)
            usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)

            cpu_time = usage_end.ru_utime - usage_start.ru_utime
            # RSS = https://en.wikipedia.org/wiki/Resident_set_size
            memory = usage_end.ru_maxrss / 1024.  # now in MB
            msg = "Ran '{name}' in {cpu_time:.1f}s and used {memory:.1f}MB of RAM"
            msg = msg.format(name=name, cpu_time=cpu_time, memory=memory)
            logger.info(msg)
            return result
        return __time_function
    return _time_function


def __build_hierarchy(hierarchy, path, command):
    """
        Builds a hierarchy from a python import path,
        e.g. run.condor.test will be parsed into a dictionary of
        {"run":{
            "this": <command>, # if "run" is a valid command by itself
            "condor":{
                "test": {
                    "this": <command>
                    }
                }
            }
        }
    """
    import collections
    path = path.replace('.', ' ')
    if ' ' in path:
        elements = path.split(' ')
        current = elements[0]
        if not current in hierarchy:
            hierarchy[current] = collections.OrderedDict()
        new_path = ' '.join(elements[1:])
        __build_hierarchy(hierarchy[current], new_path, command)
    else:
        hierarchy[path] = collections.OrderedDict([('this', command)])


def __get_commands(command_path):
    """
        Reads the folder sub-structure of ntp/commands and
        returns all found modules that contain a Command class.

        The folder structure
        ntp/commands/list/X
        ntp/commands/list/Y
        ntp/commands/run/X
        is mapped onto
        {
            'ntp.commands.list.X': Command class
            'ntp.commands.list.Y': Command class
            'ntp.commands.run.X': Command class
        }

    """
    import collections
    commands = collections.OrderedDict()
    hierarchy = collections.OrderedDict()
    for p, _, _ in sorted(os.walk(command_path)):
        relative_path = os.path.relpath(p, command_path)
        # If it's the current directory, ignore
        if relative_path == '.':
            continue
        # Convert directory structure to module path
        relative_path = relative_path.replace('/', '.')
        absolute_path = '{0}.{1}'.format(BASE_MODULE, relative_path)
        try:
            if sys.version_info < (2, 7):
                mod = import_module(absolute_path, fromlist=['Command'])
            else:
                mod = import_module(absolute_path)
            if hasattr(mod, 'Command'):
                if type(mod.Command) is type(object):
                    commands[relative_path] = mod.Command
                    __build_hierarchy(hierarchy, relative_path, mod.Command)
        except ImportError, e:
            import traceback
            LOG.error('Could not import {0}'.format(absolute_path))
            LOG.error(traceback.format_exc())
            continue

    return commands, hierarchy

COMMANDS, HIERARCHY = __get_commands(COMMAND_PATH)


def __traverse(commands, tokens, incomplete, results=[]):
    """
        traverses through a sub-hierarchy of the commands
        Results are writtend into the 'results' parameter.
    """
    IGNORE_KEYS = ['this']
    if not commands or commands.keys() == IGNORE_KEYS:  # end of hierarchy
        return
    n_tokens = len(tokens)
    if n_tokens > 1:
        t = tokens.pop(0)
        if t in commands:
            __traverse(commands[t], tokens, incomplete, results)
    elif n_tokens == 1:
        t = tokens.pop(0)
        if t in commands and not t in IGNORE_KEYS:
            current = commands[t]
            if incomplete:
                results.append(t)
            else:
                if len(current) > 0:
                    results.append('')
                __traverse(current, tokens, incomplete, results)
        else:
            for command in commands:
                if command.startswith(t) and not command in IGNORE_KEYS:
                    results.append(command)
    elif n_tokens == 0:
        for command in commands:
            if not command in IGNORE_KEYS:
                results.append(command)


def __complete(text, state):
    """
        autocompletes partial commands
    """
    buffer = readline.get_line_buffer()
    incomplete = True
    if len(buffer) > 0 and buffer[-1] == ' ':
        incomplete = False
    tokens = buffer.split()

    results = []
    __traverse(HIERARCHY, tokens, incomplete, results)
    f = lambda x: x + ' '
    results = map(f, results)
    return results[state]


def __execute(command, parameters, variables):
    rc = False
    try:
        rc = command.run(parameters, variables)
    except Exception:
        import traceback
        LOG.error('Command failed: ' + traceback.format_exc())

    text = command.get_text()
    if len(text) > 0:
        LOG.info(text)
    if rc is True:
        return 0
    return -1


def _convert(value):
    """
        Converts a string value to either bool, int or float as applicable
    """
    s = str(value).strip().lower()
    if s in ['false', 'n', '0']:
        return False
    if s in ['true', 'y', '1']:
        return True

    # next try float
    try:
        f = float(s)
        return f
    except ValueError:
        LOG.debug('Could not convert "{0}" to bool'.format(value))

    # otherwise assume string
    return value


def _parse_args(args):
    positional_args = []
    variables = {}
    for arg in args:
        if '=' in arg:
            name, value = arg.split('=')

            variables[name] = _convert(value)
        else:
            positional_args.append(arg)
    return positional_args, variables


def _find_command_and_args(cli_input):
    command = None
    args = []
    for i in range(len(cli_input), 0, -1):
        relative_path = '.'.join(cli_input[:i])
        if relative_path in COMMANDS:
            command = COMMANDS[relative_path]()
            args = cli_input[i:]
            break
    return command, args


def run_cli(prompt=PROMPT):
    """ sets up command line interface"""

    readline.set_completer(__complete)
    readline.parse_and_bind(COMPLETEKEY + ": complete")

    done = 0
    while not done:
        try:
            cmd = raw_input(prompt)
            readline.write_history_file(HISTFILE)
            if cmd in ['exit', 'quit', 'q']:
                run_command(['quit'])
                done = 1
            else:
                run_command(shlex.split(cmd))
        except EOFError:
            print()
            done = 1
        except KeyboardInterrupt:
            print()
            done = 1


def run_command(args):
    if not args:
        return

    command, arguments = _find_command_and_args(args)
    parameters, variables = _parse_args(arguments)

    if command is None:
        LOG.error('Invalid command "{0}"'.format(args[0]))
        LOG.info('Known commands:\n' + '\n '.join(COMMANDS.keys()))
        return -1

    # log command
    # execute
    return __execute(command, parameters, variables)


def call(cmd_and_args, logger, stdout_log_level=logging.DEBUG, stderr_log_level=logging.ERROR, **kwargs):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    From: https://gist.github.com/bgreenlee/1402841
    """
    logger.debug('executing: {0}'.format(cmd_and_args))
    child = subprocess.Popen(cmd_and_args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)

    log_level = {child.stdout: stdout_log_level,
                 child.stderr: stderr_log_level}

    outputs = {child.stdout: '',
               child.stderr: ''}

    def check_io():
        ready_to_read = select.select(
            [child.stdout, child.stderr], [], [], 1)[0]
        for io in ready_to_read:
            line = io.readline()
            outputs[io] += line[:-1]
            logger.log(log_level[io], line[:-1])

    # keep checking stdout/stderr until the child exits
    while child.poll() is None:
        check_io()

    check_io()  # check again to catch anything after the process exits

    return_code = child.wait()
    stdout, stderr = outputs.values()

    # fix for stupid cmsenv behaviour
    # (cmsenv will cause the stdout to go to stderr instead)
    if 'CMSSW_BASE' in os.environ and stdout == '':
        msg = 'CMSSW_BASE is set which causes stdout to '
        msg += 'go to stderr instead. Copying stderr to stdout to fix this.'
        logger.warning(msg)
        stdout = stderr

    return return_code, stdout, stderr
