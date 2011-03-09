from BristolAnalysis.NTupleTools.runBasics_MC_cfi import process

process.source.fileNames = cms.untracked.vstring(
            'file:/storage/TopQuarkGroup/mc/ttbarAODSIM38X.root'
            )
process.TFileService.fileName = 'testNtupler_MC.root'

process.maxEvents.input = 100