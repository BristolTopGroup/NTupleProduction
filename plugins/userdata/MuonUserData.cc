// -*- C++ -*-
//
// Package:    BristolAnalysis/NtupleProduction
// Class:      MuonUserData
//
/**\class NtupleProduction MuonUserData.cc BristolAnalysis/NtupleProduction/plugins/userdata/MuonUserData.cc

 Description: Adds derived data to the muon collection

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
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

namespace ntp {
namespace userdata {

//
// class declaration
//

class MuonUserData: public edm::stream::EDProducer<> {
public:
	explicit MuonUserData(const edm::ParameterSet&);
	~MuonUserData();

	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginStream(edm::StreamID) override;
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	bool isLoose(const pat::Muon& muon) const;
	bool isGood(const pat::Muon& muon) const;
	void fillVertexVariables(const edm::Event&, pat::Muon& el) const;

	// inputs
	edm::EDGetToken muonInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
	const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag_;

	// cuts
	double minLooseMuonPt_, maxLooseMuonEta_;
	double minSignalMuonPt_, maxSignalMuonEta_;
	double looseMuonIso_, tightMuonIso_, controlMuonIso1_, controlMuonIso2_;

	//
	reco::Vertex primaryVertex_;
	bool hasGoodPV_, useBeamSpotCorrection_;

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
MuonUserData::MuonUserData(const edm::ParameterSet& iConfig) :
				muonInputTag_(
						consumes < std::vector
								< pat::Muon >> (iConfig.getParameter < edm::InputTag > ("muonCollection"))),
				vtxInputTag_(
						consumes < std::vector
								< reco::Vertex >> (iConfig.getParameter < edm::InputTag > ("vertexCollection"))), //
				beamSpotInputTag_(
						consumes < reco::BeamSpot > (iConfig.getParameter < edm::InputTag > ("beamSpotCollection"))), //
				minLooseMuonPt_(iConfig.getParameter<double>("minLooseMuonPt")), //
				maxLooseMuonEta_(iConfig.getParameter<double>("maxLooseMuonEta")), //
				minSignalMuonPt_(iConfig.getParameter<double>("minSignalMuonPt")), //
				maxSignalMuonEta_(iConfig.getParameter<double>("maxSignalMuonEta")), //
				looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //
				tightMuonIso_(iConfig.getParameter<double>("tightMuonIsolation")), //
				controlMuonIso1_(iConfig.getParameter<double>("controlMuonIsolation1")), //
				controlMuonIso2_(iConfig.getParameter<double>("controlMuonIsolation2")), //
				primaryVertex_(), //
				hasGoodPV_(false), //
				useBeamSpotCorrection_(iConfig.getParameter<bool>("useBeamSpotCorrection")) {
	//register your products
	produces<std::vector<pat::Muon> >();
	//now do what ever other initialization is needed
}

MuonUserData::~MuonUserData() {

	// do anything here that needs to be done at destruction time
	// (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ method called to produce the data  ------------
void MuonUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < std::vector<pat::Muon> > muons;
	iEvent.getByToken(muonInputTag_, muons);

	edm::Handle < reco::BeamSpot > bsHandle;
	iEvent.getByToken(beamSpotInputTag_, bsHandle);

	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);

	if (primaryVertices.isValid()) {
		if (primaryVertices->size() >= 1) {
			primaryVertex_ = primaryVertices->front();
			hasGoodPV_ = true;
		} else
			hasGoodPV_ = false;
	}

	if (muons.isValid()) {
		std::auto_ptr < std::vector<pat::Muon> > muonCollection(new std::vector<pat::Muon>(*muons));
		size_t nMuons = muonCollection->size();
		LogDebug("NTupleTools|MuonUserData") << "Total # Muons: " << nMuons;

		for (size_t index = 0; index < nMuons; ++index) {
			pat::Muon& mu = muonCollection->at(index);
			bool hasTrack = mu.isGlobalMuon() || mu.isTrackerMuon();

			//isolation
			mu.addUserFloat("PFRelIso03", getRelativeIsolation(mu, 0.3, false));
			mu.addUserFloat("PFRelIso04", getRelativeIsolation(mu, 0.4, false));
			mu.addUserFloat("PFRelIso03DeltaBeta", getRelativeIsolation(mu, 0.3, true));
			mu.addUserFloat("PFRelIso04DeltaBeta", getRelativeIsolation(mu, 0.4, true));

			// vertex association
			fillVertexVariables(iEvent, mu);
			// beamspot correction
			double trkd0 = -9999.;
			if (hasTrack) {
				trkd0 = mu.track()->d0();
				if (useBeamSpotCorrection_ && bsHandle.isValid()) {
					trkd0 = -(mu.track()->dxy(bsHandle->position()));
				}
			}

			mu.addUserFloat("trkd0", trkd0);

			// Top Object Definitions
			mu.addUserInt("isLoose", isLoose(mu));
			bool isGood = this->isGood(mu);
			double iso = mu.userFloat("PFRelIso04DeltaBeta");
			mu.addUserInt("isGood", isGood && iso < tightMuonIso_);
			mu.addUserInt("isGoodNonIsoR1", isGood && iso > controlMuonIso1_);
			mu.addUserInt("isGoodNonIsoR2", isGood && iso > controlMuonIso2_ && iso < controlMuonIso1_);

		}
		iEvent.put(muonCollection);
	}
}

bool MuonUserData::isLoose(const pat::Muon& muon) const {
	bool passesPt = muon.pt() > minLooseMuonPt_;
	bool passesEta = fabs(muon.eta()) < maxLooseMuonEta_;
	bool passesId = muon.isLooseMuon();
	bool passesIso = muon.userFloat("PFRelIso04DeltaBeta") < looseMuonIso_;
	return passesPt && passesEta && passesId && passesIso;
}

bool MuonUserData::isGood(const pat::Muon& muon) const {
	bool passesPt = muon.pt() > minSignalMuonPt_;
	bool passesEta = fabs(muon.eta()) < maxSignalMuonEta_;
	bool passesId = false;

	if (hasGoodPV_) {
		passesId = muon.isTightMuon(primaryVertex_);
	}

	return passesPt && passesEta && passesId;
}

void MuonUserData::fillVertexVariables(const edm::Event& iEvent, pat::Muon& mu) const {
	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);

	size_t index = 9999;
	double minVtxDist3D = 9999.;
	double vtxDistZ = -9999.;
	bool hasTrack = mu.isGlobalMuon() || mu.isTrackerMuon();

	if (primaryVertices.isValid() && hasTrack) {
		LogDebug("MuonUserData") << "Total # Primary Vertices: " << primaryVertices->size();
		// this is only for the primary vertex

		for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it != primaryVertices->end();
				++v_it) {

			double distXY = mu.track()->dxy(v_it->position());
			double distZ = mu.track()->dz(v_it->position());
			double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

			if (dist3D < minVtxDist3D) {
				minVtxDist3D = dist3D;
				index = size_t(std::distance(primaryVertices->begin(), v_it));
				vtxDistZ = distZ;
			}
		}
	}
	// closest vertex
	mu.addUserInt("vtxIndex", index);
	mu.addUserFloat("vtxDistZ", vtxDistZ);
	// primary vertex
	mu.addUserFloat("primaryVertexDXY", mu.dB());
	mu.addUserFloat("primaryVertexDXYError", mu.edB());
	// beamspot
	mu.addUserFloat("beamSpotDXY", mu.dB(pat::Muon::BS2D));
	mu.addUserFloat("beamSpotDXYError", mu.edB(pat::Muon::BS2D));
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void MuonUserData::beginStream(edm::StreamID) {
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void MuonUserData::endStream() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void MuonUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE (MuonUserData);
} //userdata
} //ntp
