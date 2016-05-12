"""
    setup:  sets up the workspace area with CMSSW and the dependencies

        Usage:
            setup [ntp tag] [force=true]

        Parameters:
            ntp tag:  specifies which version of NTP to load. Default is
                      'run2:latest' which is equal to 'master'

            force:    forces workspace to be deleted if it already exists.
"""

from __future__ import print_function
import json
import shutil
import os
import sys
import optparse
import subprocess

from .. import Command as C


def setup_cmssw(workspace, version):
    commands = [
        'cd {workspace}',
        'source /cvmfs/cms.cern.ch/cmsset_default.sh',
        '/cvmfs/cms.cern.ch/common/scram project CMSSW {cmssw_version}',
        'cd {cmssw_version}/src',
        'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
        'git cms-init'
    ]
    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one.format(workspace=workspace, cmssw_version=version)
    subprocess.call(all_in_one, shell=True)


def setup_dependencies(workspace, dependencies):
    commands = [
        'cd {workspace}',
        'source /cvmfs/cms.cern.ch/cmsset_default.sh',
        'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
    ]

    for dep in dependencies:
        print('Setting up dependency "{0}"'.format(dep['name']))
        provider = dep['provider']
        source = dep['source']
        destination = dep['destination']
        command = ''
        if provider == 'git':
            command = 'git clone {source} {destination}'.format(
                source=source, destination=destination)
        elif provider == 'git-cms-merge-topic':
            command = 'git-cms-merge-topic {source}'.format(source=source)
        else:
            print('Unknown provider "{0}"'.format(provider))
            sys.exit()
        commands.append(command)
        if 'setup-cmds' in dep:
            commands.extend(dep['setup-cmds'])

    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one.format(workspace=workspace)
    subprocess.call(all_in_one, shell=True)


def link_ntp(cmssw_workspace, destination, links):
    NTPROOT = os.environ['NTPROOT']

    c1 = 'mkdir -p {workspace}/{destination}'.format(
        workspace=cmssw_workspace,
        destination=destination
    )
    commands = [c1]

    for l in links:
        command = 'ln -s {NTPROOT}/{link} {workspace}/{destination}/{link}'
        command = command.format(NTPROOT=NTPROOT,
                                 link=l,
                                 workspace=cmssw_workspace,
                                 destination=destination)
        commands.append(command)

    all_in_one = ' && '.join(commands)
    subprocess.call(all_in_one, shell=True)


def compile_workspace(workspace, n_jobs=1):
    n_jobs = 1
    commands = [
        'cd {workspace}',
        'source /cvmfs/cms.cern.ch/cmsset_default.sh',
        'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
        'scram b jobs={n_jobs}'
    ]

    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one.format(workspace=workspace, n_jobs=n_jobs)
    subprocess.call(all_in_one, shell=True)


def get_metadata():
    NTPROOT = os.environ['NTPROOT']
    metadata = {}
    with open(NTPROOT + '/metadata.json') as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


def get_cmssw_workspace():
    NTPROOT = os.environ['NTPROOT']
    metadata = get_metadata()

    workspace = '{root}/workspace/{cmssw_version}/src'
    workspace = workspace.format(
        root=NTPROOT, cmssw_version=metadata['cmssw_version'])
    return workspace


class Command(C):

    DEFAULTS = {
        'force': False,
    }

    def __init__(self):
        super(Command, self).__init__(__file__, __doc__)

    def run(self, args, variables):

        if not self.__is_ready_to_go():
            self.__text = "Could not find environmental variable 'NTPROOT'\n"
            self.__text += "You need to run 'source bin/env.sh' first!"

        self.__prepare(args, variables)

        NTPROOT = os.environ['NTPROOT']
        ntp_tag = 'run2:latest'  # == master
        if args:
            ntp_tag = args[0]

        metadata = get_metadata()
        workspace = NTPROOT + '/workspace'

        if os.path.exists(workspace):
            print('Workspace already exists')
            if self.__variables['force']:
                print('Deleting existing workspace')
                if os.path.exists(workspace + '.save'):
                    shutil.rmtree(workspace + '.save')
                shutil.move(workspace, workspace + '.save')
            else:
                sys.exit(-1)

        print('Creating workspace')
        os.mkdir(workspace)
        os.mkdir(workspace + '/cache')
        os.mkdir(workspace + '/log')
        os.mkdir(workspace + '/results')
        os.mkdir(workspace + '/tmp')
        cmssw_version = metadata['cmssw_version']
        setup_cmssw(workspace, cmssw_version)

        # set up NTP
        cmssw_workspace = workspace + '/{0}/src'.format(cmssw_version)
        destination = metadata['destination']
        links = metadata['links']
        link_ntp(cmssw_workspace, destination, links)

        dependencies = metadata['dependencies']
        setup_dependencies(cmssw_workspace, dependencies)

        compile_workspace(cmssw_workspace)

        return True

    def __is_ready_to_go(self):
        return 'NTPROOT' in os.environ
