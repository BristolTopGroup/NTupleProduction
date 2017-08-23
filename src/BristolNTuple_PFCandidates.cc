#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFCandidates.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/ESHandle.h"

using namespace std;

BristolNTuple_PFCandidates::BristolNTuple_PFCandidates(const edm::ParameterSet& iConfig) :
        // pfcandidateToken_( consumes<std::vector<pat::PackedCandidate>  >( iConfig.getParameter<edm::InputTag> ( "pfCandidatesTag" ) ) ),
        pfcandidateToken_( consumes<std::vector<reco::PFCandidate>  >( iConfig.getParameter<edm::InputTag> ( "pfCandidatesTag" ) ) ),
		electronsToken_( consumes < std::vector<pat::Electron>	> (iConfig.getParameter < edm::InputTag > ("electrons"))),
		muonsToken_( consumes < std::vector<pat::Muon>	> (iConfig.getParameter < edm::InputTag > ("muons")))
		{
        produces < std::vector<reco::PFJet> > ("OneJet");
}

void BristolNTuple_PFCandidates::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr< std::vector<reco::PFJet> > EventJetCollection( new std::vector<reco::PFJet>());

    edm::Handle<std::vector<pat::PackedCandidate>  > pfCandidateCollection;
    iEvent.getByToken( pfcandidateToken_, pfCandidateCollection );

    // edm::Handle<std::vector<reco::PFCandidate>  > pfCandidateCollection;
    // iEvent.getByToken( pfcandidateToken_, pfCandidateCollection );

	// Electrons
	edm::Handle < std::vector<pat::Electron> > electrons;
	iEvent.getByToken(electronsToken_, electrons);
	electrons_ = *electrons;

	bool hasSignalElectron = false;
	if ( electrons_.size() > 0 ) {
		hasSignalElectron = true;
	}

	// Muons
	edm::Handle < std::vector<pat::Muon> > muons;
	iEvent.getByToken(muonsToken_, muons);
	muons_ = *muons;

	bool hasSignalMuon = false;
	if ( muons_.size() > 0 ) {
		hasSignalMuon = true;
	}

    reco::PFJet dummyJet;
	
	int numPFCandidates = pfCandidateCollection->size();
	for ( int iPFCandidate = 0; iPFCandidate < numPFCandidates; ++iPFCandidate ) {
	    edm::Ptr<pat::PackedCandidate> pfCandidatePtr(pfCandidateCollection, iPFCandidate);
	    // edm::Ptr<reco::PFCandidate> pfCandidatePtr(pfCandidateCollection, iPFCandidate);
	    if ( pfCandidatePtr->pt() > 1 && fabs( pfCandidatePtr->eta() ) < 2.4 ) {

	    	if ( hasSignalElectron ) {
	    		double dr_toElectron = deltaR(electrons_[0].eta(), electrons_[0].phi(), pfCandidatePtr->eta(), pfCandidatePtr->phi());
	    		if ( dr_toElectron < 0.01 ) continue;
	    	}

	    	if ( hasSignalMuon ) {
	    		double dr_toMuon = deltaR(muons_[0].eta(), muons_[0].phi(), pfCandidatePtr->eta(), pfCandidatePtr->phi());
	    		if ( dr_toMuon < 0.01 ) continue;
	    	}
		    dummyJet.addDaughter( pfCandidatePtr );
	    }
	}
	EventJetCollection->push_back(dummyJet);
	iEvent.put(EventJetCollection, "OneJet");
}





