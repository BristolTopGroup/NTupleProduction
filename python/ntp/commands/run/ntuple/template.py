PYCONF = """
import FWCore.ParameterSet.Config as cms
from BristolAnalysis.NTupleTools.run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName='{OUTPUT_FILE}'

# In order to work around the limitation of 255 parameters to a python function
# we pass 1 tuple of all the files to the vstring function
# see
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePoolInputSources#Example_3_More_than_255_input_fi
process.source.fileNames = cms.untracked.vstring(
*(
{input_files},
)
)

process.jetUserData.btagCalibrationFile = cms.string('{BTAG_CALIB_FILE}')

if '{JSON_URL}':
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(url = '{JSON_URL}').getVLuminosityBlockRange()

"""
