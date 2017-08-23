#ifndef BristolNTuplePFCandidatesExtra
#define BristolNTuplePFCandidatesExtra

#include <string>
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class BristolNTuple_PFCandidates : public edm::EDProducer {
	public:
	  	explicit BristolNTuple_PFCandidates(const edm::ParameterSet&);

	private:
	  	void produce( edm::Event &, const edm::EventSetup & );
	    // const edm::EDGetTokenT<std::vector<pat::PackedCandidate>  > pfcandidateToken_;
	    const edm::EDGetTokenT<std::vector<reco::PFCandidate>  > pfcandidateToken_;
		const edm::EDGetToken electronsToken_;
		const edm::EDGetToken muonsToken_;

		pat::ElectronCollection electrons_;
		pat::MuonCollection muons_;

};

#endif
