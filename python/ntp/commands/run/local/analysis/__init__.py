"""
    run condor analysis:
        Runs the ntuple based analysis code (AnalysisSoftware) to produce the
        final set of trees.
        
    Usage:
        run local analysis dataset=<data set> campaign=<campaign>
        
    Parameters:
        campaign: which campaign to run. Corresponds to the folder
                  structure in crab/*
                  Default is 'Test'.
        dataset:  Alias for the single dataset you want to run over. Corresponds
                  to the file names (without extension) in crab/*/*.py.
                  Accepts wild-cards and comma-separated lists.
                  Default is 'TTJets_PowhegPythia8'.
                  This parameter is ignored if parameter file is given.
        files:    Instead of running on a specific dataset, run over the
                  given (comma-separated) list of files
        nevents:  Number of events to process.
                  Default is 1000.
        noop:     'NO OPeration', will not run AnalysisSoftware. Default: false
        output_file: Name of the output file. Default: atOutput.root
"""
from __future__ import print_function
import os
import logging
import glob
import shutil

from .. import Command as C
from ntp.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR
from crab.util import find_input_files

BAT_BASE = os.path.join(CMSSW_SRC, 'BristolAnalysis', 'Tools')
LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'bat.py')
OUTPUT_FILE = os.path.join(RESULTDIR, 'atOutput.root')

BASE = """
import os
import sys
from copy import deepcopy
from imp import load_source
dirname, _ = os.path.split(os.path.abspath(__file__))
analysis_info = load_source( 'analysis_info', '{BAT_BASE}/python/analysis_info.py' )

mc_path = analysis_info.mc_path_13TeV
data_path = analysis_info.data_path_13TeV
datasets = analysis_info.datasets_13TeV

analysisModes = analysis_info.analysis_modes_13TeV

available_settings = [
    'ElectronScaleFactorSystematic', 
    'MuonScaleFactorSystematic', 
    'JESsystematic', 
    'JetSmearingSystematic', 
    'PUsystematic', 
    'BTagSystematic', 
    'LightTagSystematic', 
    'custom_file_suffix'
]

default_settings = {{
    'ElectronScaleFactorSystematic':0,
    'MuonScaleFactorSystematic':0,
    'JESsystematic':0,
    'JetSmearingSystematic':0,
    'PUFile':'PileUp_2015_truth_central.root',
    'PUFile_up':'PileUp_2015_truth_up.root',
    'PUFile_down':'PileUp_2015_truth_down.root',
    'MuonIdIsoScaleFactorsFile':'nofile.root',
    'TTbarLikelihoodFile' : 'LikelihoodInputAnalyserOutput.root',
    'BTagEfficiencyFile' : 'BTagEfficiency.root',
    'BTagSystematic':0,
    'LightTagSystematic':0,
    'custom_file_suffix':'',
    'pdfWeightNumber' : 0,
}}

analysis_settings = {{
    'Electron_down':{{'ElectronScaleFactorSystematic':-1}},
    'Electron_up':{{'ElectronScaleFactorSystematic':1}},
    'Muon_down':{{'MuonScaleFactorSystematic':-1}},
    'Muon_up':{{'MuonScaleFactorSystematic':1}},
    'BJet_down':{{'BTagSystematic':-1}},
    'BJet_up':{{'BTagSystematic':1}},
    'JES_down':{{'JESsystematic':-1}},
    'JES_up':{{'JESsystematic':1}},
    'JetSmearing_up':{{'JetSmearingSystematic':1}},
    'JetSmearing_down':{{'JetSmearingSystematic':-1}},
    'LightJet_down':{{'LightTagSystematic':-1}},
    'LightJet_up':{{'LightTagSystematic':1}},
    'PU_down':{{ 'PUFile':'PileUp_2015_truth_down.root', 'custom_file_suffix':'PU_down' }},
    'PU_up':{{'PUFile':'PileUp_2015_truth_up.root', 'custom_file_suffix':'PU_up' }},
    'Test': {{'custom_file_suffix':'TESTING'}}
}}

#helper functions
def getAnalysisSettings(analysisMode):
    if not analysisMode in analysis_settings.keys():
        return default_settings
    
    settings = deepcopy(default_settings)
    settings.update(analysis_settings[analysisMode])
    return settings


#config start
#number of events to be processed
maxEvents = {nevents}# 0 == all

toolsFolder = "{BAT_BASE}"

sample = "{dataset}"
analysisMode = "{mode}"
    
settings = getAnalysisSettings(analysisMode)
if sample in ['TTJets-mcatnlo','TTJets-powheg']:
    suffixes = {{'TTJets-mcatnlo':'MCatNLO','TTJets-powheg':'POWHEG'}}
    if settings['custom_file_suffix'] == "":
        settings['custom_file_suffix'] = suffixes[sample]
    else:
        settings['custom_file_suffix'] = suffixes[sample] + '_' + settings['custom_file_suffix']    


# Option to process a single ntuple of a sample rather than all of them
ntupleToProcess = -1

#File for pile-up re-weighting
PUFile = "{BAT_BASE}/data/" + settings['PUFile']
PUFile_up = "{BAT_BASE}/data/" + settings['PUFile_up']
PUFile_down = "{BAT_BASE}/data/" + settings['PUFile_down']
getMuonScaleFactorsFromFile = True
getElectronScaleFactorsFromFile = True
ElectronIdScaleFactorsFile = '{BAT_BASE}/data/ElectronCutBasedID_MediumWP_76X_SF2D.root'
ElectronIsoScaleFactorsFile = '{BAT_BASE}/data/Elec_SF_Fit_Syst.root'
ElectronTriggerScaleFactorsFile = '{BAT_BASE}/data/ElectronTriggerEfficiencies.root'
MuonIdScaleFactorsFile = '{BAT_BASE}/data/MuonID_Z_RunCD_Reco76X_Feb15.root'
MuonIsoScaleFactorsFile = '{BAT_BASE}/data/MuonIso_Z_RunCD_Reco76X_Feb15.root'
MuonTriggerScaleFactorsFile = '{BAT_BASE}/data/SingleMuonTrigger_Z_RunCD_Reco76X_Feb15.root'
getHadronTriggerFromFile = True
hadronTriggerFile = ''
ElectronScaleFactorSystematic = settings['ElectronScaleFactorSystematic']
MuonScaleFactorSystematic = settings['MuonScaleFactorSystematic']

TTbarLikelihoodFile = "{BAT_BASE}/data/" + settings['TTbarLikelihoodFile']
BTagEfficiencyFile = "{BAT_BASE}/data/" + settings['BTagEfficiencyFile']

#JES Systematic, the +/- number of uncertainties to vary the jets with
JESsystematic = settings['JESsystematic']
JetSmearingSystematic = settings['JetSmearingSystematic']
BTagSystematic = settings['BTagSystematic']
LightTagSystematic = settings['LightTagSystematic']
custom_file_suffix = settings['custom_file_suffix']

if ntupleToProcess > 0 :
    filetype = '*%03d.root' % ntupleToProcess
    print 'Will only consider ntuple : ',filetype
    settings['custom_file_suffix'] += str(ntupleToProcess)
    custom_file_suffix = settings['custom_file_suffix']

inputFiles = inputFiles = [
{input_files},
]

print 'Parsed config settings:'
for setting,value in settings.iteritems():
    print setting, '=', value


#Jet Energy Resolutions files (L7 corrections)
bJetResoFile = "{BAT_BASE}/data/bJetReso.root"
lightJetResoFile = "{BAT_BASE}/data/lightJetReso.root"

#Jet Smearing application
applyJetSmearing = True

#Apply Top Pt reweighting
applyTopPtReweighting = False

#use HitFit for analysis
useHitFit = False
produceFitterASCIIoutput = False

#MET corrections application
applyMetSysShiftCorr = False
applyMetType0Corr = False

#relative Path from calling BAT to the TopQuarkAnalysis folder
TQAFPath = ""

#integrated luminosity the MC simulation will be scaled to
lumi = 15933 
#this value will be part of the output file name: DataType_CenterOfMassEnergyTeV_lumipb-1_....
centerOfMassEnergy = 13

#file with information (cross-section, number of processed events) for event weight calculation
datasetInfoFile = ""
if centerOfMassEnergy == 13:
    datasetInfoFile = "{BAT_BASE}/python/DataSetInfo_13TeV_25ns.py"


nTuple_version = 0

"""


class Command(C):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'files': '',
        'noop': False,
        'output_file': OUTPUT_FILE,
        'pset_template': BASE,
        'mode': 'central',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        if 'output_file' in variables:
            output_file = os.path.join(RESULTDIR, variables['output_file'])
            if not output_file.endswith('.root'):
                output_file += '.root'
            variables['output_file'] = output_file

        self.__prepare(args, variables)
#         campaign = self.__variables['campaign']
        chosen_dataset = self.__variables['dataset']
#         from BristolAnalysis.Tools.analysis_info import datasets_13TeV
        bat_path = '{0}/BristolAnalysis/Tools/python'.format(CMSSW_SRC)
        from imp import load_source
        analysis_info = load_source(
            'analysis_info', bat_path + '/analysis_info.py')
        datasets_13TeV = analysis_info.datasets_13TeV
        if not chosen_dataset in datasets_13TeV and variables['files'] == "":
            LOG.error('Cannot find dataset {0}'.format(chosen_dataset))
            return False

        input_files = []
        if variables['files'] != "":
            input_files = variables['files'].split(',')
            input_files = [os.path.abspath(f) for f in input_files]
        else:
            input_files = datasets_13TeV[chosen_dataset]
        LOG.debug(
            "Using files for NTP input:\n{0}".format('\n'.join(input_files)))

        self.__output_file = self.__variables['output_file']

        self.__write_pset(input_files)

        # making sure the correct HLT menu is read
        if 'reHLT' in input_files[0]:
            self.__variables['isReHLT'] = 1

        if not self.__variables['noop']:
            code = self.__run_analysisSoftware(
                chosen_dataset, self.__variables['mode'])
            self.__text = "Ran {PSET}\n"
            self.__text += "Logging information can be found in {LOGDIR}/ntp.log\n"
            if code == 0:
                self.__text += "Created atOutput: {OUTPUT_FILE}\n"
                self.__text = self.__text.format(
                    PSET=PSET, LOGDIR=LOGDIR, OUTPUT_FILE=self.__output_file)
            else:
                self.__text += "BAT experienced an error,"
                self.__text += " return code: {code}\n"
                self.__text = self.__text.format(
                    PSET=PSET, LOGDIR=LOGDIR, code=code)
                if code == 139:
                    LOG.warning(
                        '########################################################')
                    LOG.warning(
                        '####  Ignoring segault (hopefully) at the end of AS ####')
                    LOG.warning(
                        '########################################################')
                    return True
                return False

        else:
            LOG.info('Found "noop", not running CMSSW')

        return True

    def __write_pset(self, input_files):
        nevents = int(self.__variables['nevents'])
        input_files = self.__format_input_files(input_files)

        with open(PSET, 'w+') as f:
            content = self.__variables['pset_template'].format(
                nevents=nevents,
                input_files=input_files,
                BAT_BASE=BAT_BASE,
                maxEvents=nevents,
                mode='central',
                dataset=self.__variables['dataset'],
                #                 OUTPUT_FILE=self.__output_file,
            )
            f.write(content)

    @time_function('__run_analysisSoftware', LOG)
    def __run_analysisSoftware(self, dataset, mode):
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'sample="{dataset}" analysisMode="{mode}" BAT {PSET} {params}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            dataset=dataset,
            mode=mode,
            PSET=PSET,
            params=self.__extract_params()
        )

        LOG.info("Executing BAT")
        from ntp.interpreter import call
        code, _, _ = call(
            [all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)
        self.__move_output_files()

        return code

    def __move_output_files(self):
        output_files = glob.glob(
            '{CMSSW_SRC}/*.root'.format(CMSSW_SRC=CMSSW_SRC))

        output_file = self.__output_file
        for f in output_files:
            if 'tree_' in f:
                LOG.debug('Moving {0} -> {1}'.format(f, output_file))
                shutil.move(f, output_file)
            else:
                LOG.debug('Removing obsolete file: {0}'.format(f))
                os.remove(f)
