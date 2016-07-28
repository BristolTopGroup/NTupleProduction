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

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

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

	enum BTagWPs {
		LOOSE, MEDIUM, TIGHT, NBTagWPs,
	};

private:
	virtual void beginStream(edm::StreamID) override;
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	void fillVertexVariables(const edm::Event&, pat::Jet& jet) const;
	void fillUncertainties(pat::Jet& jet, JetCorrectionUncertainty& jecUnc) const;
	void fillJetIds(pat::Jet& jet) const;
	void fillBtagging(pat::Jet& jet) const;
	void fillBtagWeights(pat::Jet& jet) const;
	void fillJEC(pat::Jet& jet, const edm::Event& iEvent, const edm::EventSetup& iSetup,
			const JetCorrector* jetCorrector) const;
	void fillJER(pat::Jet& jet) const;

	// ----------member data ---------------------------
	// inputs
	edm::EDGetToken jetInputTag_;
	const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
	const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag_;
	std::string jecUncertainty_;
	const std::string jetCorrectionService_;
	std::string bJetDiscriminator_, btagCalibrationFile_;
	BTagCalibration btagCalibration_;
	std::vector<BTagCalibrationReader> btagReaders_;

	// cuts
	double minLooseJetPt_, maxLooseJetEta_;
	double minSignalJetPt_, maxSignalJetEta_;

	double minBtagDiscLooseWP_, minBtagDiscMediumWP_, minBtagDiscTightWP_;

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
				jetInputTag_(
						consumes < std::vector
								< pat::Jet >> (iConfig.getParameter < edm::InputTag > ("jetCollection"))), //
				vtxInputTag_(
						consumes < std::vector
								< reco::Vertex >> (iConfig.getParameter < edm::InputTag > ("vertexCollection"))), //
				beamSpotInputTag_(
						consumes < reco::BeamSpot > (iConfig.getParameter < edm::InputTag > ("beamSpotCollection"))), //
				jecUncertainty_(iConfig.getParameter < std::string > ("jecUncertainty")), //
				jetCorrectionService_(iConfig.getParameter < std::string > ("jetCorrectionService")), //
				bJetDiscriminator_(iConfig.getParameter < std::string > ("bJetDiscriminator")), //
				btagCalibrationFile_(iConfig.getParameter < std::string > ("btagCalibrationFile")), //
				btagCalibration_("csvv2", btagCalibrationFile_.c_str()), //
				btagReaders_(), //
				minSignalJetPt_(iConfig.getParameter<double>("minSignalJetPt")), //
				maxSignalJetEta_(iConfig.getParameter<double>("maxSignalJetEta")), //
				minBtagDiscLooseWP_(iConfig.getParameter<double>("minBtagDiscLooseWP")),
				minBtagDiscMediumWP_(iConfig.getParameter<double>("minBtagDiscMediumWP")),
				minBtagDiscTightWP_(iConfig.getParameter<double>("minBtagDiscTightWP")) {
	//register your products
	produces<std::vector<pat::Jet> >();
	//now do what ever other initialization is needed
	btagReaders_.reserve(size_t(BTagWPs::NBTagWPs));

	// check for updates:
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
	for (size_t index = 0; index < BTagWPs::NBTagWPs; ++index) {
		// operating point, central sys type, systematics types
		BTagCalibrationReader reader((BTagEntry::OperatingPoint) index, "central", { "up", "down" });
		reader.load(btagCalibration_, BTagEntry::FLAV_B, "mujets");
		reader.load(btagCalibration_, BTagEntry::FLAV_C, "mujets");
		reader.load(btagCalibration_, BTagEntry::FLAV_UDSG, "incl");
		btagReaders_.push_back(reader);
	}

	consumes<double>(edm::InputTag("fixedGridRhoFastjetAll"));
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
	JetCorrectorParameters const & jetCorrectorParams = (*jetCorrectorCollection)["Uncertainty"];
	JetCorrectionUncertainty jecUnc(jetCorrectorParams);
	const JetCorrector* jetCorrector(JetCorrector::getJetCorrector(jetCorrectionService_, iSetup));

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

			//IDs
			fillJetIds(jet);

			// b-tagging
			fillBtagging(jet);

			// JEC
			fillJEC(jet, iEvent, iSetup, jetCorrector);

			// only for simulation
			if (!iEvent.isRealData()) {
				fillBtagWeights(jet);
				// JER
				fillJER(jet);
			}
		}
		iEvent.put(jetCollection);
	}
}

void JetUserData::fillUncertainties(pat::Jet& jet, JetCorrectionUncertainty& jecUnc) const {
	// from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections
	jecUnc.setJetEta(jet.eta());
	jecUnc.setJetPt(jet.pt());
	double unc = jecUnc.getUncertainty(true);
	double ptUp = jet.pt() * (1 + unc);
	double ptDown = jet.pt() * (1 - unc);
	jet.addUserFloat("JECUncertainty", unc);
	jet.addUserFloat("ptUp", ptUp);
	jet.addUserFloat("ptDown", ptDown);

	//TODO: add absolute JEC factor:
	/*// get a copy of the uncorrected p4
	 reco::Candidate::LorentzVector uncorrJet = ijet->correctedP4(0);
	 // Then get the correction (L1+L2+L3 [+L2L3 for data])
	 jec_->setJetEta( uncorrJet.eta() );
	 jec_->setJetPt ( uncorrJet.pt() );
	 jec_->setJetE  ( uncorrJet.energy() );
	 jec_->setJetA  ( ijet->jetArea() );
	 jec_->setRho   ( *(rhoHandle.product()) );
	 jec_->setNPV   ( pvHandle->size() );
	 double corr = jec_->getCorrection();
	 // Here will be the working variable for all the jet energy effects
	 reco::Candidate::LorentzVector scaledJetP4 = uncorrJet * corr; */
}

void JetUserData::fillVertexVariables(const edm::Event& iEvent, pat::Jet& jet) const {
	edm::Handle < std::vector<reco::Vertex> > primaryVertices;
	iEvent.getByToken(vtxInputTag_, primaryVertices);
	if (primaryVertices.isValid()) {
		LogDebug("JetUserData") << "Total # Primary Vertices: " << primaryVertices->size();
		// this is only for the primary vertex
		reco::Vertex pv = primaryVertices->front();
		int bestVtxIndex3Ddist = -1;
		int bestVtxIndexXYdist = -1;
		int bestVtxIndexZdist = -1;

		int bestVtxIndexSharedTracks = -1;

		double minVtxDist3D = 999999.;
		double minVtxDistXY = -99999.;
		double minVtxDistZ = -99999.;
		double maxTrackAssocRatio = -9999.;

		for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it != primaryVertices->end();
				++v_it) {

			double sumweights = 0.0;
			double dist3Dweighted = 0.0;
			double distXYweighted = 0.0;
			double distZweighted = 0.0;
			double assocsumpttracks = 0.0;
			double trackassociationratio = 0.000001;

			// Loop on tracks in jet, calculate PT weighted 3D distance to vertex and PT weighted shared track ratio
			const reco::TrackRefVector &jtracks = jet.associatedTracks();
			for (reco::TrackRefVector::const_iterator jtIt = jtracks.begin(); jtIt != jtracks.end(); ++jtIt) {
				if (jtIt->isNull())
					continue;
				const reco::Track *jtrack = jtIt->get();
				double trackptweight = jtrack->pt();
				sumweights += trackptweight;

				// Weighted Distance Calculation
				double distXY = jtrack->dxy(v_it->position());
				double distZ = jtrack->dz(v_it->position());
				dist3Dweighted = trackptweight * (sqrt(pow(distXY, 2) + pow(distZ, 2)));
				distXYweighted = trackptweight * distXY;
				distZweighted = trackptweight * distZ;

				// Loop on vertex tracks, find PT weighted shared tracks.
				for (reco::Vertex::trackRef_iterator vtIt = v_it->tracks_begin(); vtIt != v_it->tracks_end(); ++vtIt) {
					if (vtIt->isNull())
						continue;
					const reco::Track *vtrack = vtIt->get();
					if (vtrack != jtrack)
						continue;
					assocsumpttracks += jtrack->pt();
					break;
				}

				trackassociationratio = assocsumpttracks / sumweights;

			}

			// Divide distances by sum of weights.
			dist3Dweighted = dist3Dweighted / sumweights;
			distXYweighted = distXYweighted / sumweights;
			distZweighted = distZweighted / sumweights;

			// Find vertex with minimum weighted distance.
			if (dist3Dweighted < minVtxDist3D) {
				minVtxDist3D = dist3Dweighted;
				bestVtxIndex3Ddist = int(std::distance(primaryVertices->begin(), v_it));

			}

			if (distXYweighted < minVtxDistXY) {
				minVtxDistXY = distXYweighted;
				bestVtxIndexXYdist = int(std::distance(primaryVertices->begin(), v_it));
			}

			if (distZweighted < minVtxDistZ) {
				minVtxDistZ = distZweighted;
				bestVtxIndexZdist = int(std::distance(primaryVertices->begin(), v_it));
			}

			// Find vertex with minimum weighted distance.
			if (trackassociationratio > maxTrackAssocRatio) {
				maxTrackAssocRatio = trackassociationratio;
				bestVtxIndexSharedTracks = int(std::distance(primaryVertices->begin(), v_it));
			}

		}
		jet.addUserFloat("bestVertexTrackAssociationFactor", maxTrackAssocRatio);
		jet.addUserInt("bestVertexTrackAssociationIndex", bestVtxIndexSharedTracks);
		jet.addUserFloat("closestVertexWeighted3DSeparation", minVtxDist3D);
		jet.addUserFloat("closestVertexWeightedXYSeparation", minVtxDistXY);
		jet.addUserFloat("closestVertexWeightedZSeparation", minVtxDistZ);
		jet.addUserInt("closestVertex3DIndex", bestVtxIndex3Ddist);
		jet.addUserInt("closestVertexXYIndex", bestVtxIndexXYdist);
		jet.addUserInt("closestVertexZIndex", bestVtxIndexZdist);
	}
}

void JetUserData::fillJetIds(pat::Jet& jet) const {
	double NHF = jet.neutralHadronEnergyFraction();
	double NEMF = jet.neutralEmEnergyFraction();
	double CHF = jet.chargedHadronEnergyFraction();
	double MUF = jet.muonEnergyFraction();
	double CEMF = jet.chargedEmEnergyFraction();
	size_t NumConst = jet.chargedMultiplicity() + jet.neutralMultiplicity();
	size_t NumNeutralParticle = jet.neutralMultiplicity();
	size_t CHM = jet.chargedMultiplicity();

	double eta = jet.eta();

	bool looseJetId(false);
	bool tightJetId(false);
	bool tightLepVetoJetId(false);
	// from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
	if (abs(eta) <= 3.0) {
		looseJetId = (NHF < 0.99 && NEMF < 0.99 && NumConst > 1)
				&& ((abs(eta) <= 2.4 && CHF > 0 && CHM > 0 && CEMF < 0.99) || abs(eta) > 2.4);
		tightJetId = (NHF < 0.90 && NEMF < 0.90 && NumConst > 1)
				&& ((abs(eta) <= 2.4 && CHF > 0 && CHM > 0 && CEMF < 0.99) || abs(eta) > 2.4);
		tightLepVetoJetId = (NHF < 0.90 && NEMF < 0.90 && NumConst > 1 && MUF < 0.8)
				&& ((abs(eta) <= 2.4 && CHF > 0 && CHM > 0 && CEMF < 0.90) || abs(eta) > 2.4);
	} else {
		looseJetId = (NEMF < 0.90 && NumNeutralParticle > 10);
		tightJetId = (NEMF < 0.90 && NumNeutralParticle > 10);
	}

	jet.addUserInt("looseJetId", looseJetId);
	jet.addUserInt("tightJetId", tightJetId);
	jet.addUserInt("tightLepVetoJetId", tightLepVetoJetId);

	bool passesEta(fabs(jet.eta()) < maxSignalJetEta_);
	bool passesPt(jet.pt() > minSignalJetPt_);
	bool passesPtDown(jet.userFloat("ptDown") > minSignalJetPt_);
	bool passesPtUp(jet.userFloat("ptUp") > minSignalJetPt_);

	bool passesIdAndEta = looseJetId && passesEta;
	jet.addUserInt("passesEta", passesEta);
	jet.addUserInt("passesPt", passesPt);
	jet.addUserInt("passesPtDown", passesPtDown);
	jet.addUserInt("passesPtUp", passesPtUp);

	jet.addUserInt("isGood", passesIdAndEta && passesPt);
	jet.addUserInt("isGoodPtDown", passesIdAndEta && passesPtDown);
	jet.addUserInt("isGoodPtUp", passesIdAndEta && passesPtUp);

}

void JetUserData::fillBtagging(pat::Jet& jet) const {
	double bDisc = jet.bDiscriminator(bJetDiscriminator_);
	bool passesLooseBtagWP = bDisc > minBtagDiscLooseWP_;
	bool passesMediumBtagWP = bDisc > minBtagDiscMediumWP_;
	bool passesTightBtagWP = bDisc > minBtagDiscTightWP_;
	jet.addUserFloat("btagDiscriminator", bDisc);
	jet.addUserInt("passesLooseBtagWP", passesLooseBtagWP);
	jet.addUserInt("passesMediumBtagWP", passesMediumBtagWP);
	jet.addUserInt("passesTightBtagWP", passesTightBtagWP);

}

void JetUserData::fillBtagWeights(pat::Jet& jet) const {
	std::vector<std::string> prefixes = {"loose", "medium", "tight"};
	unsigned int bQuark = 5;
	unsigned int cQuark = 4;
	unsigned int jet_flavour = jet.hadronFlavour();
//	bool isBOrCQuark = jet_flavour == bQuark || jet_flavour == cQuark;

	for (size_t index = 0; index < BTagWPs::NBTagWPs; ++index) {
		std::string prefix = prefixes.at(index);
		BTagEntry::JetFlavor bEntry = BTagEntry::FLAV_UDSG;
		if(jet_flavour == bQuark) {
			bEntry = BTagEntry::FLAV_B;
		}
		if(jet_flavour == cQuark) {
			bEntry = BTagEntry::FLAV_C;
		}
		BTagCalibrationReader reader = btagReaders_.at(index);
		double weight = reader.eval_auto_bounds("central", bEntry, jet.eta(), jet.pt());
		double weightUp = reader.eval_auto_bounds("up", bEntry, jet.eta(), jet.pt());
		double weightDown = reader.eval_auto_bounds("down", bEntry, jet.eta(), jet.pt());

		jet.addUserFloat(prefix + "BTagWeight", weight);
		jet.addUserFloat(prefix + "BTagWeightUp", weightUp);
		jet.addUserFloat(prefix + "BTagWeightDown", weightDown);
	}
}

void JetUserData::fillJEC(pat::Jet& jet, const edm::Event& iEvent, const edm::EventSetup& iSetup,
		const JetCorrector* jetCorrector) const {
	double jec = jetCorrector->correction(jet.correctedJet("Uncorrected"), iEvent, iSetup);
	jet.addUserFloat("JEC", jec);
	jet.addUserFloat("L2L3ResJEC", jet.pt() / jet.correctedJet("L3Absolute").pt());
	jet.addUserFloat("L3AbsJEC", jet.correctedJet("L3Absolute").pt() / jet.correctedJet("L2Relative").pt());
	jet.addUserFloat("L2RelJEC", jet.correctedJet("L2Relative").pt() / jet.correctedJet("L1FastJet").pt());
	jet.addUserFloat("L1OffJEC", jet.correctedJet("L1FastJet").pt() / jet.correctedJet("Uncorrected").pt());
}

void JetUserData::fillJER(pat::Jet& jet) const {

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
