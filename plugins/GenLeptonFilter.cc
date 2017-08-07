#include "BristolAnalysis/NTupleTools/plugins/GenLeptonFilter.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
// system include files
#include <memory>
#include <iostream>
// user include files
#include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

GenLeptonFilter::GenLeptonFilter(const edm::ParameterSet& iConfig) :
    particleLevelLeptonSelectionInput_( consumes< reco::GenJetCollection >(iConfig.getParameter<edm::InputTag>("particleLevelLeptonSelectionInput"))),
    prefix_(iConfig.getParameter<std::string>  ("Prefix")),
    minPt_(iConfig.getParameter<double> ("minPt")),
    maxAbsoluteEta_(iConfig.getParameter<double> ("maxAbsoluteEta")){
	produces<bool>(prefix_ + "OneParticleLepton");

}

void GenLeptonFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("particleLevelLeptonSelectionInput");
	desc.addUntracked < std::string > ("prefix", "Event.");
	desc.add < double > ("minPt", 20);
	desc.add < double > ("maxAbsoluteEta", 2.4);
}

GenLeptonFilter::~GenLeptonFilter() {
}

bool GenLeptonFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	bool singleLepton(false);
	int nLepton = 0;
	int pdgId;

	if (!iEvent.isRealData()) {

		edm::Handle < reco::GenJetCollection > particleLeptons;
		iEvent.getByToken(particleLevelLeptonSelectionInput_, particleLeptons);

		if (particleLeptons.isValid()) {
			for (reco::GenJetCollection::const_iterator it = particleLeptons->begin(); it != particleLeptons->end(); ++it) {
				if (it->pt() < minPt_ || fabs(it->eta()) > maxAbsoluteEta_) 
					continue;
				pdgId = abs(it->pdgId());
				if ( pdgId == 11 || pdgId == 13 ) {
					nLepton++;
				}
			}
		} 
	}

	if(nLepton == 1){ 
		singleLepton=true;
	}
	iEvent.put(std::auto_ptr<bool>(new bool(singleLepton)), prefix_ + "OneParticleLepton");
	return singleLepton;
}

// ------------ method called once each job just before starting event loop  ------------
void GenLeptonFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void GenLeptonFilter::endJob() {
}

void GenLeptonFilter::beginRun() {
}

//define this as a plug-in
DEFINE_FWK_MODULE (GenLeptonFilter);
