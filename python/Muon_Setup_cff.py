def setup_muons(process, cms, options):
	print '=' * 60
	print "Setting up Bad Muon Filters"
	print '=' * 60

	process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
	process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
	process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
	process.BadPFMuonFilter.taggingMode = cms.bool(True)

	process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
	process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
	process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
	process.BadChargedCandidateFilter.taggingMode = cms.bool(True)

	process.badMuonTagger = cms.Sequence(process.BadPFMuonFilter + process.BadChargedCandidateFilter)
