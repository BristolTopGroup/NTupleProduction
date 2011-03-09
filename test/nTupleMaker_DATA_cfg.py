from BristolAnalysis.NTupleTools.runBasics_DATA_cfi import process

process.source.fileNames = cms.untracked.vstring(
            'file:/storage/TopQuarkGroup/data/Nov4ReReco_example.root'
            )
process.TFileService.fileName = 'testNtupler_DATA.root'

process.maxEvents.input = 100