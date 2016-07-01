// -*- C++ -*-
//
// Package:    BristolAnalysis/NtupleProduction
// Class:      JetUserData
//
/**\class NtupleProduction JetUserData.cc BristolAnalysis/NtupleProduction/plugins/userdata/JetUserData.cc

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

namespace ntp {
namespace userdata {

//
// class declaration
//

class JetUserData: public edm::stream::EDProducer<> {
public:
	explicit JetUserData(const edm::ParameterSet&);
	~JetUserData();

	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginStream(edm::StreamID) override;
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	bool isGood(const pat::Jet& jet) const;
	void fillVertexVariables(const edm::Event&, pat::Jet& jet) const;
	void fillUncertainties(pat::Jet& jet, JetCorrectionUncertainty& jecUnc) const;

	// inputs
	edm::EDGetToken jetInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
	const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag_;
	std::string jecUncertainty_;

	// cuts
	double minLooseJetPt_, maxLooseJetEta_;
	double minSignalJetPt_, maxSignalJetEta_;

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
JetUserData::JetUserData(const edm::ParameterSet& iConfig) :
		jetInputTag_(consumes < std::vector < pat::Jet >> (iConfig.getParameter < edm::InputTag > ("jetCollection"))), //
		vtxInputTag_(
				consumes < std::vector < reco::Vertex >> (iConfig.getParameter < edm::InputTag > ("vertexCollection"))), //
		beamSpotInputTag_(consumes < reco::BeamSpot > (iConfig.getParameter < edm::InputTag > ("beamSpotCollection"))), //
		jecUncertainty_(iConfig.getParameter < std::string > ("jecUncertainty")), //
		minLooseJetPt_(iConfig.getParameter<double>("minLooseJetPt")), //
		maxLooseJetEta_(iConfig.getParameter<double>("maxLooseJetEta")), //
		minSignalJetPt_(iConfig.getParameter<double>("minSignalJetPt")), //
		maxSignalJetEta_(iConfig.getParameter<double>("maxSignalJetEta")) {
	//register your products
	produces<std::vector<pat::Jet> >();
	//now do what ever other initialization is needed
}

JetUserData::~JetUserData() {

	// do anything here that needs to be done at destruction time
	// (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ method called to produce the data  ------------
void JetUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < std::vector<pat::Jet> > jets;
	iEvent.getByToken(jetInputTag_, jets);

	edm::Handle < reco::BeamSpot > bsHandle;
	iEvent.getByToken(beamSpotInputTag_, bsHandle);

	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);

	edm::ESHandle < JetCorrectorParametersCollection > jetCorrectorCollection;
	iSetup.get<JetCorrectionsRecord>().get(jecUncertainty_, jetCorrectorCollection);
	JetCorrectorParameters const & jetCorrector = (*jetCorrectorCollection)["Uncertainty"];
	JetCorrectionUncertainty jecUnc(jetCorrector);

//	bool isSimulation = !iEvent.isRealData();

	// https://twiki.cern.ch/twiki/bin/view/CMS/JetEnergyScale
	// https://twiki.cern.ch/twiki/bin/view/CMS/JECAnalysesRecommendations

	if (jets.isValid()) {
		std::auto_ptr < std::vector<pat::Jet> > jetCollection(new std::vector<pat::Jet>(*jets));
		size_t nJets = jetCollection->size();
		LogDebug("NTupleTools|JetUserData") << "Total # Jets: " << nJets;

		for (size_t index = 0; index < nJets; ++index) {
			pat::Jet & jet = jetCollection->at(index);
			fillUncertainties(jet, jecUnc);
			// we need to be able to add 4 vector with different
			// JEC and JER
			// probably just adding a scale factor would be good

			// vertex association
			fillVertexVariables(iEvent, jet);

			// Top Object Definitions
			jet.addUserInt("isGood", isGood(jet) && jet.pt() > minSignalJetPt_);
			jet.addUserInt("isGoodPtUp", isGood(jet) && jet.userFloat("ptUp") > minSignalJetPt_);
			jet.addUserInt("isGoodPtDown", isGood(jet) && jet.userFloat("ptDown") > minSignalJetPt_);

		}
		iEvent.put(jetCollection);
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

bool JetUserData::isGood(const pat::Jet& jet) const {
	bool passesEta(fabs(jet.eta()) < maxSignalJetEta_);
	bool passesJetID(false);
	bool passNOD = jet.numberOfDaughters() > 1;
	bool passNHF = jet.neutralHadronEnergyFraction() + jet.HFHadronEnergyFraction() < 0.99;
	bool passNEF = jet.neutralEmEnergyFraction() < 0.99;
	bool passCHF = true;
	bool passNCH = true;
	bool passCEF = true;
	if (fabs(jet.eta()) < 2.4) {
		passCEF = jet.chargedEmEnergyFraction() < 0.99;
		passCHF = jet.chargedHadronEnergyFraction() > 0;
		passNCH = jet.chargedMultiplicity() > 0;
	}
	passesJetID = passNOD && passCEF && passNHF && passNEF && passCHF && passNCH;

	return passesEta && passesJetID;
}

void JetUserData::fillUncertainties(pat::Jet& jet, JetCorrectionUncertainty& jecUnc) const {
	// from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections
	jecUnc.setJetEta(jet.eta());
	jecUnc.setJetPt(jet.pt());
	double unc = jecUnc.getUncertainty(true);
	double ptUp = jet.pt() * (1 + unc);
	double ptDown = jet.pt() * (1 - unc);
	jet.addUserFloat("ptUp", ptUp);
	jet.addUserFloat("ptDown", ptDown);
}

void JetUserData::fillVertexVariables(const edm::Event& iEvent, pat::Jet& jet) const {
	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);

	if (primaryVertices.isValid()) {
		LogDebug("JetUserData") << "Total # Primary Vertices: " << primaryVertices->size();
		// this is only for the primary vertex
		reco::Vertex pv = primaryVertices->front();

		for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it != primaryVertices->end();
				++v_it) {
		}
	}
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void JetUserData::beginStream(edm::StreamID) {
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void JetUserData::endStream() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void JetUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE (JetUserData);
} //userdata
} //ntp
