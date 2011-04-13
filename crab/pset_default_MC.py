import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.runBasics_MC_cfi import process
process.source.fileNames = cms.untracked.vstring(
            'file:/storage/top/mc/ttbarAODSIM38X.root'
            )
# reduce stdout
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)
#process.MessageLogger.cerr.INFO.limit = 10
#process.MessageLogger.cerr.threshold = 'ERROR'

process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')

#use online skimming
process.EventFilter.minNElectrons = 1
process.EventFilter.minElectronPt = 25.