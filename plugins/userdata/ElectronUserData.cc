// -*- C++ -*-
//
// Package:    BristolAnalysis/NtupleProduction
// Class:      ElectronUserData
//
/**\class NtupleProduction ElectronUserData.cc BristolAnalysis/NtupleProduction/plugins/userdata/ElectronUserData.cc

 Description: Adds derived data to the electron collection

 */
//
// Original Author: kreczko
//         Created:  Fri, 17 Jun 2016 16:15:30 GMT
//
//
// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/VIDCutFlowResult.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

namespace ntp {
namespace userdata {

//
// class declaration
//

class ElectronUserData: public edm::stream::EDProducer<> {
public:
	explicit ElectronUserData(const edm::ParameterSet&);
	~ElectronUserData();

	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginStream(edm::StreamID) override;
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	float getEA(float);
	bool isMatchedWithTrigger(const pat::Electron, trigger::TriggerObjectCollection, int&);
	bool passIDWP(std::string WP, bool isEB, float dEtaIn, float dPhiIn, float full5x5, float hoe, float d0, float dz,
			float ooemoop, bool conv, int missHits);

	bool passesInvertedIDCuts(const vid::CutFlowResult fullCutFlowData, std::vector<uint> invertedSelection);

	// inputs
	const edm::EDGetToken electronInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
	const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Conversion> > conversionsInputTag_;

	const edm::EDGetTokenT<edm::ValueMap<bool> > mediumElectronIDMapToken_;
	const edm::EDGetTokenT<edm::ValueMap<vid::CutFlowResult> > eleMediumIdFullInfoMapToken_;

	edm::ValueMap<bool> mediumElectronIDDecisions_;
	edm::ValueMap<vid::CutFlowResult> medium_id_cutflow_data_;

	// cuts
	double maxLooseElectronEta_, minLooseElectronPt_;

	// ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
ElectronUserData::ElectronUserData(const edm::ParameterSet& iConfig) :
				electronInputTag_(
						consumes < std::vector
								< pat::Electron >> (iConfig.getParameter < edm::InputTag > ("electronCollection"))),
				vtxInputTag_(
						consumes < std::vector
								< reco::Vertex >> (iConfig.getParameter < edm::InputTag > ("vertexCollection"))), //
				beamSpotInputTag_(
						consumes < reco::BeamSpot > (iConfig.getParameter < edm::InputTag > ("beamSpotCollection"))), //
				conversionsInputTag_(
						consumes < std::vector
								< reco::Conversion >> (iConfig.getParameter < edm::InputTag > ("conversionInput"))), //
				mediumElectronIDMapToken_(
						consumes < edm::ValueMap<bool>
								> (iConfig.getParameter < edm::InputTag > ("mediumElectronIDMap"))), //
				eleMediumIdFullInfoMapToken_(
						consumes < edm::ValueMap<vid::CutFlowResult>
								> (iConfig.getParameter < edm::InputTag > ("mediumElectronIDMap"))) {
	//register your products
	produces<std::vector<pat::Electron> >();
	//now do what ever other initialization is needed
}

ElectronUserData::~ElectronUserData() {

	// do anything here that needs to be done at destruction time
	// (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ method called to produce the data  ------------
void ElectronUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < std::vector<pat::Electron> > electrons;
	iEvent.getByToken(electronInputTag_, electrons);

	edm::Handle < reco::BeamSpot > bsHandle;
	iEvent.getByToken(beamSpotInputTag_, bsHandle);

	edm::Handle < std::vector<reco::Conversion> > hConversions;
	iEvent.getByToken(conversionsInputTag_, hConversions);

	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);
	edm::Handle < edm::ValueMap<bool> > medium_id_decisions;
	iEvent.getByToken(mediumElectronIDMapToken_, medium_id_decisions);
	mediumElectronIDDecisions_ = *medium_id_decisions;

	edm::Handle < edm::ValueMap<vid::CutFlowResult> > medium_id_cutflow_data;
	iEvent.getByToken(eleMediumIdFullInfoMapToken_, medium_id_cutflow_data);
	medium_id_cutflow_data_ = *medium_id_cutflow_data;

	if (electrons.isValid()) {
		std::auto_ptr < std::vector<pat::Electron> > electronCollection(new std::vector<pat::Electron>(*electrons));
		size_t nElectrons = electronCollection->size();
		LogDebug("NTupleTools|ElectronUserData") << "Total # Electrons: " << nElectrons;

		for (size_t index = 0; index < nElectrons; ++index) {
			pat::Electron & el = electronCollection->at(index);
			el.addUserInt("isLoose", 0);
		}
		iEvent.put(electronCollection);
	}

	/* This is an event example
	 //Read 'ExampleData' from the Event
	 Handle<ExampleData> pIn;
	 iEvent.getByLabel("example",pIn);

	 //Use the ExampleData to create an ExampleData2 which
	 // is put into the Event
	 std::unique_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
	 iEvent.put(std::move(pOut));
	 */

	/* this is an EventSetup example
	 //Read SetupData from the SetupRecord in the EventSetup
	 ESHandle<SetupData> pSetup;
	 iSetup.get<SetupRecord>().get(pSetup);
	 */
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void ElectronUserData::beginStream(edm::StreamID) {
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void ElectronUserData::endStream() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ElectronUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE (ElectronUserData);
} //userdata
} //ntp
