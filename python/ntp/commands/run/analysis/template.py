PYCONF = """
import os
import sys
from copy import deepcopy
from imp import load_source
dirname, _ = os.path.split(os.path.abspath(__file__))

opj = os.path.join

BAT_BASE = "{BAT_BASE}"
BAT_PYTHON = opj(BAT_BASE, 'python')
BAT_DATA = opj(BAT_BASE, 'data')
analysis_info_file = opj(BAT_PYTHON, 'analysis_info_2016.py')
analysis_info = load_source('analysis_info', analysis_info_file)

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
    'ElectronScaleFactorSystematic': 0,
    'MuonScaleFactorSystematic': 0,
    'JESsystematic': 0,
    'JetSmearingSystematic': 0,
    'PUFile':'PileUp_2015_truth_central.root',
    'PUFile_up':'PileUp_2015_truth_up.root',
    'PUFile_down':'PileUp_2015_truth_down.root',
    'MuonIdScaleFactorsFile': 'EfficienciesAndSF_COMBINED.root',
    'MuonIsoScaleFactorsFile': 'EfficienciesAndSF_Isolation_COMBINED.root',
    'MuonTriggerScaleFactorsFile': 'EfficienciesAndSF_Trigger_COMBINED.root',
    'MuonTrackingScaleFactorsFile': 'Tracking_EfficienciesAndSF_BCDEFGH.root',
    'ElectronTriggerScaleFactorsFile': 'EfficienciesAndSF_ElectronTrigger_COMBINED.root',
    'ElectronIdScaleFactorsFile' : 'egammaEffi.txt_EGM2D_id.root',
    'ElectronRecoScaleFactorsFile' : 'egammaEffi.txt_EGM2D_reco.root',
    'TTbarLikelihoodFile': 'LikelihoodInputAnalyserOutput.root',
    'BTagEfficiencyFile': 'BTagEfficiency.root',
    'BTagSystematic': 0,
    'LightTagSystematic': 0,
    'custom_file_suffix': '',
    'pdfWeightNumber': 0,
}}

analysis_settings = {{
    'Electron_down': {{'ElectronScaleFactorSystematic': -1}},
    'Electron_up': {{'ElectronScaleFactorSystematic': 1}},
    'Muon_down': {{'MuonScaleFactorSystematic': -1}},
    'Muon_up': {{'MuonScaleFactorSystematic': 1}},
    'BJet_down': {{'BTagSystematic': -1}},
    'BJet_up': {{'BTagSystematic': 1}},
    'JES_down': {{'JESsystematic': -1}},
    'JES_up': {{'JESsystematic': 1}},
    'JetSmearing_up': {{'JetSmearingSystematic': 1}},
    'JetSmearing_down': {{'JetSmearingSystematic': -1}},
    'LightJet_down': {{'LightTagSystematic': -1}},
    'LightJet_up': {{'LightTagSystematic': 1}},
    'PU_down':{{ 'PUFile':'PileUp_2015_truth_down.root', 'custom_file_suffix':'PU_down' }},
    'PU_up':{{'PUFile':'PileUp_2015_truth_up.root', 'custom_file_suffix':'PU_up' }},
    'Test': {{'custom_file_suffix': 'TESTING'}}
}}

# helper functions


def getAnalysisSettings(analysisMode):
    if not analysisMode in analysis_settings.keys():
        return default_settings

    settings = deepcopy(default_settings)
    settings.update(analysis_settings[analysisMode])
    return settings


# config start
# number of events to be processed
maxEvents = {nevents}  # 0 == all

sample = "{dataset}"
analysisMode = "{mode}"

settings = getAnalysisSettings(analysisMode)
if sample in ['TTJets-mcatnlo', 'TTJets-powheg']:
    suffixes = {{'TTJets-mcatnlo': 'MCatNLO', 'TTJets-powheg': 'POWHEG'}}
    if settings['custom_file_suffix'] == "":
        settings['custom_file_suffix'] = suffixes[sample]
    else:
        settings['custom_file_suffix'] = suffixes[
            sample] + '_' + settings['custom_file_suffix']


# Option to process a single ntuple of a sample rather than all of them
ntupleToProcess = -1

#File for pile-up re-weighting
PUFile = opj(BAT_DATA, settings['PUFile'] )
PUFile_up = opj(BAT_DATA, settings['PUFile_up'] )
PUFile_down = opj(BAT_DATA, settings['PUFile_down'] )
getMuonScaleFactorsFromFile = True
getElectronScaleFactorsFromFile = True
ElectronIdScaleFactorsFile = opj(BAT_DATA, 'egammaEffi.txt_EGM2D_id.root')
ElectronRecoScaleFactorsFile = opj(BAT_DATA, 'egammaEffi.txt_EGM2D_reco.root')
ElectronTriggerScaleFactorsFile = opj(
    BAT_DATA, 'EfficienciesAndSF_ElectronTrigger_COMBINED.root')
MuonIdScaleFactorsFile = opj(BAT_DATA, 'EfficienciesAndSF_COMBINED.root')
MuonIsoScaleFactorsFile = opj(BAT_DATA, 'EfficienciesAndSF_Isolation_COMBINED.root')
MuonTriggerScaleFactorsFile = opj(BAT_DATA,'EfficienciesAndSF_Trigger_COMBINED.root')
MuonTrackingScaleFactorsFile = opj(BAT_DATA, 'Tracking_EfficienciesAndSF_BCDEFGH.root' )
getHadronTriggerFromFile = True
hadronTriggerFile = ''
ElectronScaleFactorSystematic = settings['ElectronScaleFactorSystematic']
MuonScaleFactorSystematic = settings['MuonScaleFactorSystematic']

TTbarLikelihoodFile = opj(BAT_DATA, settings['TTbarLikelihoodFile'])
BTagEfficiencyFile = opj(BAT_DATA, settings['BTagEfficiencyFile'])

# JES Systematic, the +/- number of uncertainties to vary the jets with
JESsystematic = settings['JESsystematic']
JetSmearingSystematic = settings['JetSmearingSystematic']
BTagSystematic = settings['BTagSystematic']
LightTagSystematic = settings['LightTagSystematic']
custom_file_suffix = settings['custom_file_suffix']

if ntupleToProcess > 0:
    filetype = '*%03d.root' % ntupleToProcess
    print 'Will only consider ntuple : ', filetype
    settings['custom_file_suffix'] += str(ntupleToProcess)
    custom_file_suffix = settings['custom_file_suffix']

inputFiles = [
{input_files},
]

print 'Parsed config settings:'
for setting, value in settings.iteritems():
    print setting, '=', value


# Jet Energy Resolutions files (L7 corrections)
bJetResoFile = opj(BAT_DATA, 'bJetReso.root')
lightJetResoFile = opj(BAT_DATA, 'lightJetReso.root')

# Jet Smearing application
applyJetSmearing = True

# Apply Top Pt reweighting
applyTopPtReweighting = False

# use HitFit for analysis
useHitFit = False
produceFitterASCIIoutput = False

# MET corrections application
applyMetSysShiftCorr = False
applyMetType0Corr = False

# relative Path from calling BAT to the TopQuarkAnalysis folder
TQAFPath = ""

# integrated luminosity the MC simulation will be scaled to
lumi = 35900
# this value will be part of the output file name:
# DataType_CenterOfMassEnergyTeV_lumipb-1_....
centerOfMassEnergy = 13

# file with information (cross-section, number of processed events) for
# event weight calculation
datasetInfoFile = ""
if centerOfMassEnergy == 13:
    datasetInfoFile = opj(BAT_PYTHON, 'DataSetInfo_13TeV_25ns.py')


nTuple_version = 0

"""
