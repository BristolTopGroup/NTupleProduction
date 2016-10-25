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

#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

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

	bool isMatchedWithTrigger(const pat::Electron, trigger::TriggerObjectCollection, int&);

	bool passesInvertedIDCuts(const vid::CutFlowResult fullCutFlowData, std::vector<uint> invertedSelection) const;
	bool isVeto(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const;
	bool isGood(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const;
	bool passesImpactParameterSelection(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const;
	void fillVertexVariables(const edm::Event&, pat::Electron& el) const;

	// inputs
	edm::EDGetToken electronInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
	const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Conversion> > conversionsInputTag_;

	const edm::EDGetTokenT<edm::ValueMap<bool> > vetoElectronIDMapToken_;
	const edm::EDGetTokenT<edm::ValueMap<bool> > tightElectronIDMapToken_;
	const edm::EDGetTokenT<edm::ValueMap<vid::CutFlowResult> > eleTightIdFullInfoMapToken_;

	edm::ValueMap<bool> tightElectronIDDecisions_, vetoElectronIDDecisions_;
	edm::ValueMap<vid::CutFlowResult> tightIdCutFlowData_;

	// cuts
	double minVetoElectronPt_, maxVetoElectronEta_;
	double minSignalElectronPt_, maxSignalElectronEta_;

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
				vetoElectronIDMapToken_(
						consumes < edm::ValueMap<bool>
								> (iConfig.getParameter < edm::InputTag > ("electronVetoIdMap"))), //
				tightElectronIDMapToken_(
						consumes < edm::ValueMap<bool>
								> (iConfig.getParameter < edm::InputTag > ("electronTightIdMap"))), //
				eleTightIdFullInfoMapToken_(
						consumes < edm::ValueMap<vid::CutFlowResult>
								> (iConfig.getParameter < edm::InputTag > ("electronTightIdMap"))), //
				minVetoElectronPt_(iConfig.getParameter<double>("minVetoElectronPt")), //
				maxVetoElectronEta_(iConfig.getParameter<double>("maxVetoElectronEta")), //
				minSignalElectronPt_(iConfig.getParameter<double>("minSignalElectronPt")), //
				maxSignalElectronEta_(iConfig.getParameter<double>("maxSignalElectronEta")) {
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

	edm::Handle < edm::ValueMap<bool> > veto_id_decisions;
	iEvent.getByToken(vetoElectronIDMapToken_, veto_id_decisions);
	vetoElectronIDDecisions_ = *veto_id_decisions;

	edm::Handle < edm::ValueMap<bool> > tight_id_decisions;
	iEvent.getByToken(tightElectronIDMapToken_, tight_id_decisions);
	tightElectronIDDecisions_ = *tight_id_decisions;

	edm::Handle < edm::ValueMap<vid::CutFlowResult> > tight_id_cutflow_data;
	iEvent.getByToken(eleTightIdFullInfoMapToken_, tight_id_cutflow_data);
	tightIdCutFlowData_ = *tight_id_cutflow_data;

	if (electrons.isValid()) {
		std::auto_ptr < std::vector<pat::Electron> > electronCollection(new std::vector<pat::Electron>(*electrons));
		size_t nElectrons = electronCollection->size();
		LogDebug("NTupleTools|ElectronUserData") << "Total # Electrons: " << nElectrons;

		for (size_t index = 0; index < nElectrons; ++index) {
			pat::Electron & el = electronCollection->at(index);
			const edm::Ptr<pat::Electron> elPtr(electrons, index);
			std::vector < uint > idCutsToInvert { 99 };

			vid::CutFlowResult fullCutFlowDataTight = tightIdCutFlowData_[elPtr];
			el.addUserInt("passesVetoId", vetoElectronIDDecisions_[elPtr]);
			el.addUserInt("passesTightId", tightElectronIDDecisions_[elPtr]);
			idCutsToInvert = {7};
			// (*HEEP_id_cutflow_data)[ elPtr ].getCutFlowResultMasking(maskCuts).cutFlowPassed();
			el.addUserInt("passesTightNonIsoId", passesInvertedIDCuts(fullCutFlowDataTight, idCutsToInvert));
			idCutsToInvert = {8, 9};
			el.addUserInt("passesTightConversionId", passesInvertedIDCuts(fullCutFlowDataTight, idCutsToInvert));
			el.addUserFloat("PFRelIsoWithEA", fullCutFlowDataTight.getValueCutUpon(7));

			bool matchesConv = false;
			if (hConversions.isValid() && bsHandle.isValid()) {
				/* Conversion (fit)
				 * See https://indico.cern.ch/getFile.py/access?contribId=12&sessionId=0&resId=0&materialId=slides&confId=133587
				 * and
				 * https://hypernews.cern.ch/HyperNews/CMS/get/egamma/999.html ( N.1 )
				 */
				matchesConv = ConversionTools::hasMatchedConversion(*elPtr, hConversions, bsHandle->position());
			}
			el.addUserInt("hasMatchedConvPhot", matchesConv);

			// vertex association
			fillVertexVariables(iEvent, el);

			// Top Object Definitions
			el.addUserInt("isVeto", isVeto(elPtr, *primaryVertices));
			el.addUserInt("isGood", isGood(elPtr, *primaryVertices) && el.userInt("passesTightId"));
			el.addUserInt("isGoodNonIso", isGood(elPtr, *primaryVertices) && el.userInt("passesTightNonIsoId"));
			el.addUserInt("isGoodConversion", isGood(elPtr, *primaryVertices) && el.userInt("passesTightConversionId"));

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

/**
 *
 * @param fullCutFlowData: The versioned id (VID) cutflow result
 * @param invertedSelection a vector of ID steps to invert
 * @return
 *
 * Electron ID steps
 *  // ID Cuts
 *  // Index : Name
 *  //-----------------------------------------
 *  //   0   : MinPtCut
 *  //   1   : GsfEleSCEtaMultiRangeCut
 *  //   2   : GsfEleDEtaInCut
 *  //   3   : GsfEleDPhiInCut
 *  //   4   : GsfEleFull5x5SigmaIEtaIEtaCut
 *  //   5   : GsfEleHadronicOverEMCut
 *  //   6   : GsfEleEInverseMinusPInverseCut
 *  //   7   : GsfEleEffAreaPFIsoCut
 *  //   8  : GsfEleConversionVetoCut
 *  //   9  : GsfEleMissingHitsCut
 */

bool ElectronUserData::passesInvertedIDCuts(const vid::CutFlowResult fullCutFlowData,
		std::vector<uint> invertedSelection) const {

	bool passesFullSelection = true;
	for (uint icut = 0; icut < fullCutFlowData.cutFlowSize(); icut++) {
		bool passesThisCut = fullCutFlowData.getCutResultByIndex(icut);
		for (auto invertedCut = invertedSelection.begin(); invertedCut != invertedSelection.end(); invertedCut++) {
			if (icut == *invertedCut)
				passesThisCut = !passesThisCut;
		}
		if (!passesThisCut) {
			passesFullSelection = false;
			break;
		}
	}
	return passesFullSelection;
}

bool ElectronUserData::isVeto(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const {
	bool passesPt = electron->pt() > minVetoElectronPt_;
	bool passesEta = fabs(electron->eta()) < maxVetoElectronEta_;
	bool passesId = vetoElectronIDDecisions_[electron];
	bool passesImpactParameter = passesImpactParameterSelection( electron, primaryVertices );
	return passesPt && passesEta && passesId && passesImpactParameter;
}

bool ElectronUserData::isGood(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const {
	bool passesPtAndEta = electron->pt() > minSignalElectronPt_ && fabs(electron->eta()) < maxSignalElectronEta_;
	bool notInCrack = fabs(electron->superCluster()->eta()) < 1.4442 || fabs(electron->superCluster()->eta()) > 1.5660;
	bool inECAL = fabs(electron->superCluster()->eta()) < 2.5;
	bool passesImpactParameter = passesImpactParameterSelection( electron, primaryVertices );

	return passesPtAndEta && notInCrack && inECAL && passesImpactParameter;
}

bool ElectronUserData::passesImpactParameterSelection(const edm::Ptr<pat::Electron>& electron, std::vector<reco::Vertex> primaryVertices) const {

	// https://github.com/cms-sw/cmssw/blob/86088d61d757bad0e55addda14859c5ea6108d84/RecoEgamma/ElectronIdentification/plugins/cuts/GsfEleDxyCut.cc
	// https://github.com/cms-sw/cmssw/blob/86088d61d757bad0e55addda14859c5ea6108d84/RecoEgamma/ElectronIdentification/plugins/cuts/GsfEleDzCut.cc
	const float dxyCutValue = 
	    ( std::abs(electron->superCluster()->position().eta()) < 1.479 ? 
	      0.05 : 0.1 );

	const float dzCutValue = 
	    ( std::abs(electron->superCluster()->position().eta()) < 1.479 ? 
	      0.1 : 0.2 );

	const double dxy = ( primaryVertices.size() ? 
			       electron->gsfTrack()->dxy(primaryVertices[0].position()) : 
			       electron->gsfTrack()->dxy() );


	const double dz = ( primaryVertices.size() ? 
		      electron->gsfTrack()->dz(primaryVertices[0].position()) : 
		      electron->gsfTrack()->dz() );

	bool passesD0Selection = std::abs(dxy) < dxyCutValue;
	bool passesDZSelection = std::abs(dz) < dzCutValue;

	return passesD0Selection && passesDZSelection;
}


void ElectronUserData::fillVertexVariables(const edm::Event& iEvent, pat::Electron& el) const {
	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);

	size_t index = 9999;
	double minVtxDist3D = 9999.;
	double vtxDistZ = -9999.;
	double vtxDistXY_Corr = -9999.;
	double vtxDistZ_Corr = -9999.;

	if (primaryVertices.isValid()) {
		LogDebug("ElectronUserData") << "Total # Primary Vertices: " << primaryVertices->size();
		// this is only for the primary vertex
		reco::Vertex pv = primaryVertices->front();
		vtxDistXY_Corr = el.gsfTrack()->d0() - pv.x() * sin(el.gsfTrack()->phi()) + pv.y() * cos(el.gsfTrack()->phi());
		vtxDistZ_Corr = (el.vz() - pv.z())
				- ((el.vx() - pv.x()) * el.px() + (el.vy() - pv.y()) * el.py()) / el.pt() / el.pt() * el.pz();

		for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it != primaryVertices->end();
				++v_it) {

			double distXY = el.gsfTrack()->dxy(v_it->position());
			double distZ = el.gsfTrack()->dz(v_it->position());
			double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

			if (dist3D < minVtxDist3D) {
				minVtxDist3D = dist3D;
				index = size_t(std::distance(primaryVertices->begin(), v_it));
				vtxDistZ = distZ;
			}
		}
	}
	// closest vertex
	el.addUserInt("vtxIndex", index);
	el.addUserFloat("vtxDistZ", vtxDistZ);
	// primary vertex
	el.addUserFloat("primaryVertexDXY", el.dB());
	el.addUserFloat("primaryVertexDXYError", el.edB());
	el.addUserFloat("vtxDistXY_Corr", vtxDistXY_Corr);
	el.addUserFloat("vtxDistZ_Corr", vtxDistZ_Corr);
	// beamspot
	el.addUserFloat("beamSpotDXY", el.dB(pat::Electron::BS2D));
	el.addUserFloat("beamSpotDXYError", el.edB(pat::Electron::BS2D));
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
