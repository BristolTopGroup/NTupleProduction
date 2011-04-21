from BristolAnalysis.NTupleTools.runBasics_MC_cfi import process

process.source.fileNames = cms.untracked.vstring(
            'file:/storage/TopQuarkGroup/TT_ZuneZ2_Spring11.root'
            )
process.TFileService.fileName = 'testNtupler_MC.root'

process.maxEvents.input = 100

process.EventFilter.minNElectrons = 1
process.EventFilter.minElectronPt = 25.