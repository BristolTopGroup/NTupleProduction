// -*- C++ -*-
//
// Package:    BristolAnalysis/NtupleProduction
// Class:      IndexProducer
//
/**\class NtupleProduction IndexProducer.cc BristolAnalysis/NtupleProduction/plugins/userdata/IndexProducer.cc

 Description: Adds derived data to the jet collection

 */
//
// Original Author: kreczko
//         Created:  Fri, 25 Jun 2016 16:15:30 GMT
//
//
// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

namespace ntp {

//
// class declaration
//

class IndexProducer: public edm::stream::EDProducer<> {
public:
	typedef std::vector<unsigned int> IndexCollection;
	explicit IndexProducer(const edm::ParameterSet&);
	~IndexProducer();

	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginStream(edm::StreamID) override;
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	// ----------member data ---------------------------
	std::string name_;
	// inputs
	const edm::EDGetToken originalToken_, newToken_;

};

//
// constructors and destructor
//
IndexProducer::IndexProducer(const edm::ParameterSet& iConfig) :
				name_(iConfig.getParameter < std::string > ("outputName")), //
				originalToken_(
						consumes < edm::View<reco::Candidate>
								> (iConfig.getParameter < edm::InputTag > ("originalCollection"))), //
				newToken_(
						consumes < edm::View<reco::Candidate>
								> (iConfig.getParameter < edm::InputTag > ("newCollection"))) {
	//register your products
	produces < IndexCollection > (name_);
}

IndexProducer::~IndexProducer() {

	// do anything here that needs to be done at destruction time
	// (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ method called to produce the data  ------------
void IndexProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	std::auto_ptr<IndexCollection> indices(new IndexCollection());

	edm::Handle < edm::View<reco::Candidate> > originalCollection;
	iEvent.getByToken(originalToken_, originalCollection);

	edm::Handle < edm::View<reco::Candidate> > newCollection;
	iEvent.getByToken(newToken_, newCollection);

	for (size_t origIndex = 0; origIndex < originalCollection->size(); ++origIndex) {
		for (size_t newIndex = 0; newIndex < newCollection->size(); ++newIndex) {
			if (originalCollection->at(origIndex).p4() == newCollection->at(newIndex).p4()) {
				indices->push_back(origIndex);
			}
		}
	}

	iEvent.put(indices, name_);
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void IndexProducer::beginStream(edm::StreamID) {
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void IndexProducer::endStream() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void IndexProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE (IndexProducer);
} //ntp
