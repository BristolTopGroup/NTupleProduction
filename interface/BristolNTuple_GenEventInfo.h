#ifndef BristolNTupleGenEventInfo
#define BristolNTupleGenEventInfo

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <boost/array.hpp>

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
namespace TTbarDecay {
enum value {
	NotTtbar,
	FullHadronic,
	SemiLeptonicElectron,
	SemiLeptonicMuon,
	SemiLeptonicTau,
	FullLeptonicEE,
	FullLeptonicMuMu,
	FullLeptonicTauTau,
	FullLeptonicETau,
	FullLeptonicEMu,
	FullLeptonicMuTau,
	NumberOfDecayModes
};
}
class BristolNTuple_GenEventInfo: public edm::EDProducer {

public:
	explicit BristolNTuple_GenEventInfo(const edm::ParameterSet&);

private:
	void initLumiWeights();
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag genEvtInfoInputTag;
	const std::vector<edm::InputTag> ttbarDecayFlags_;
	const edm::InputTag puWeightsInputTag_;
	const bool storePDFWeights_, isTTbarMC_;
	const edm::InputTag pdfWeightsInputTag_;
	const edm::InputTag pileupInfoSrc_;
	const edm::InputTag tt_gen_event_input_;
	const std::string prefix_, suffix_;
};

#endif
