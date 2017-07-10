#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFCandidates.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/ESHandle.h"

using namespace std;

BristolNTuple_PFCandidates::BristolNTuple_PFCandidates(const edm::ParameterSet& iConfig) :
        // pfcandidateToken_( consumes<std::vector<pat::PackedCandidate>  >( iConfig.getParameter<edm::InputTag> ( "pfCandidatesTag" ) ) ){
        pfcandidateToken_( consumes<std::vector<reco::PFCandidate>  >( iConfig.getParameter<edm::InputTag> ( "pfCandidatesTag" ) ) ){
        produces < std::vector<reco::PFJet> > ("OneJet");
}

void BristolNTuple_PFCandidates::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr< std::vector<reco::PFJet> > EventJetCollection( new std::vector<reco::PFJet>());

    // edm::Handle<std::vector<pat::PackedCandidate>  > pfCandidateCollection;
    // iEvent.getByToken( pfcandidateToken_, pfCandidateCollection );

    edm::Handle<std::vector<reco::PFCandidate>  > pfCandidateCollection;
    iEvent.getByToken( pfcandidateToken_, pfCandidateCollection );

    reco::PFJet dummyJet;
	
	int numPFCandidates = pfCandidateCollection->size();
	for ( int iPFCandidate = 0; iPFCandidate < numPFCandidates; ++iPFCandidate ) {
	    // edm::Ptr<pat::PackedCandidate> pfCandidatePtr(pfCandidateCollection, iPFCandidate);
	    edm::Ptr<reco::PFCandidate> pfCandidatePtr(pfCandidateCollection, iPFCandidate);
	    if ( pfCandidatePtr->pt() > 1 && fabs( pfCandidatePtr->eta() ) < 2.4 ) {
		    dummyJet.addDaughter( pfCandidatePtr );
	    }
	}
	EventJetCollection->push_back(dummyJet);
	iEvent.put(EventJetCollection, "OneJet");
}





