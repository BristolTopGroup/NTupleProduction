from BristolAnalysis.NTupleTools.runBasics_DATA_cfi import process

process.source.fileNames = cms.untracked.vstring(
            'file:/storage/TopQuarkGroup/ElectronHad_Run2011A_AOD.root'
            )
process.TFileService.fileName = 'testNtupler_DATA.root'

process.maxEvents.input = 100