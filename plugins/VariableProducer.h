#ifndef VARIABLEPRODUCER
#define VARIABLEPRODUCER

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/GenericParticle.h"
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace ntp {

/**
 * Class to derive new variables from data
 */
class VariableProducer: public edm::EDProducer {
public:
	explicit VariableProducer(const edm::ParameterSet&);
	typedef math::XYZTLorentzVectorD LorentzVector;

private:
	void produce(edm::Event &, const edm::EventSetup &);

	// inputs
	const edm::EDGetTokenT<pat::JetCollection> cleanedJetsToken_;
	const edm::EDGetTokenT<pat::JetCollection> cleanedBJetsToken_;
	const edm::EDGetTokenT<pat::ElectronCollection> signalElectronToken_;
	const edm::EDGetTokenT<pat::MuonCollection> signalMuonToken_;
	const edm::EDGetTokenT<pat::METCollection> metToken_;

	const double minJetPtForHT_;
	const std::string prefix_, suffix_, channel_;

	pat::JetCollection cleanedJets_;
	pat::JetCollection cleanedBJets_;
	pat::ElectronCollection signalElectrons_;
	pat::MuonCollection signalMuons_;
	pat::MET met_;
	LorentzVector lepton_p4_;

	void setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup);

public:
	/*
	 * Calculates the hadronic energy in the events based on @jets.
	 * Only takes into accounts jets with pT > minJetPt
	 */
	static double HT(const pat::JetCollection& jets, double minJetPt);
	/*
	 * Calculates the total activity in the event based on
	 *  - HT(see VariableProducer::HT)
	 *  - signal lepton pT
	 *  - the missing transverse energy (MET)
	 */
	static double ST(const pat::JetCollection&, const LorentzVector&, const pat::MET&, double minJetPt);
	/*
	 * Calculates the invariant mass of three jets. The jets are selected such
	 * that the vector-sum of their pTs is maximised.
	 */
	static double M3(const pat::JetCollection&);
	/*
	 * Calculates the invariant mass of a lepton and the closest jet to it
	 */
	static double M_bl(const pat::Jet& b_jet, const LorentzVector&);
	/*
	 * Calculates the 3D angle between a lepton and the closest jet to it
	 */
	static double angle_bl(const pat::Jet& b_jet, const LorentzVector&);
	/*
	 * Calculates the transverse mass of a lepton and MET
	 */
	static double MT(const LorentzVector&, const pat::MET&);
	/*
	 * Calculates the transverse momentum of a particle made from a lepton and
	 * MET (a W boson candidate)
	 */
	static double WPT(const LorentzVector&, const pat::MET&);

};
}
#endif
