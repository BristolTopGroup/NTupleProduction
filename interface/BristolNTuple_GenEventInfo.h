#ifndef BristolNTupleGenEventInfo
#define BristolNTupleGenEventInfo

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <boost/array.hpp>

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "TopQuarkAnalysis/TopTools/interface/JetPartonMatching.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
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
	virtual void beginRun(edm::Run const& /* iR */, edm::EventSetup const& /* iE */);

private:
	void initLumiWeights();
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag genEvtInfoInputTag;
	const edm::InputTag   genJetsInputTag_;
	const std::vector<edm::InputTag> ttbarDecayFlags_;
	const edm::InputTag puWeightsInputTag_;
	const bool storePDFWeights_, isTTbarMC_;
	const edm::InputTag pdfWeightsInputTag_;
	const edm::InputTag pileupInfoSrc_;
	const edm::InputTag tt_gen_event_input_;
	const double minGenJetPt_, maxGenJetAbsoluteEta_;
	const std::string prefix_, suffix_;
};

#endif
