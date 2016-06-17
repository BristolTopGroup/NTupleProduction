// -*- C++ -*-
//
// Package:    BristolAnalysis/ElectronUserData
// Class:      ElectronUserData
//
/**\class ElectronUserData ElectronUserData.cc BristolAnalysis/ElectronUserData/plugins/ElectronUserData.cc

 Description: [one line class summary]

 Implementation:
 [Notes on implementation]
 */
//
// Original Author:
//         Created:  Fri, 17 Jun 2016 16:15:30 GMT
//
//
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

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
ElectronUserData::ElectronUserData(const edm::ParameterSet& iConfig) {
	//register your products
	/* Examples
	 produces<ExampleData2>();

	 //if do put with a label
	 produces<ExampleData2>("label");

	 //if you want to put into the Run
	 produces<ExampleData2,InRun>();
	 */
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
	using namespace edm;
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
