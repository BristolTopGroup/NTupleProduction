'''
    Setup script for NtupleProduction
    Usage:
    python setup.py <release tag> [-f]
'''
from __future__ import print_function
import json
import shutil
import os
import sys
import optparse
import subprocess


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

    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one.format(workspace=workspace)
    subprocess.call(all_in_one, shell=True)


def link_ntp(cmssw_workspace, destination, links):
    absolute_path = os.path.dirname(os.path.abspath(__file__))

    c1 = 'mkdir -p {workspace}/{destination}'.format(
        workspace=cmssw_workspace,
        destination=destination
    )
    commands = [c1]

    for l in links:
        command = 'ln -s {absolute_path}/{link} {workspace}/{destination}/{link}'
        command = command.format(absolute_path=absolute_path,
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

if __name__ == '__main__':
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-f", "--force",
                      action="store_true", dest="force", default=False,
                      help="force workspace to be deleted first if it already exists.")
    (options, args) = parser.parse_args()

    ntp_tag = 'run2:latest'  # == master
    if args:
        ntp_tag = args[0]

    with open('metadata.json') as metadata_file:
        metadata = json.load(metadata_file)
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        workspace = absolute_path + '/workspace'

        if os.path.exists(workspace):
            print('Workspace already exists')
            if options.force:
                print('Deleting existing workspace')
                shutil.rmtree(workspace)
            else:
                sys.exit(-1)

        os.mkdir(workspace)
        cmssw_version = metadata['cmssw_version']
        setup_cmssw(workspace, cmssw_version)

        cmssw_workspace = workspace + '/{0}/src'.format(cmssw_version)
        dependencies = metadata['dependencies']
        setup_dependencies(cmssw_workspace, dependencies)

        destination = metadata['destination']
        links = metadata['links']
        link_ntp(cmssw_workspace, destination, links)

        compile_workspace(cmssw_workspace)
