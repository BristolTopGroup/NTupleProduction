#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "BristolAnalysis/NTupleTools/plugins/VariableProducer.h"
#include "DataFormats/Math/interface/angle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

namespace ntp {
VariableProducer::VariableProducer(const edm::ParameterSet& iConfig) :
				cleanedJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedJets"))), //
				cleanedBJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedBJets"))), //
				signalElectronToken_(
						consumes < pat::ElectronCollection
								> (iConfig.getParameter < edm::InputTag > ("signalElectrons"))), //
				signalMuonToken_(
						consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("signalMuons"))), //
				metToken_(consumes < pat::METCollection > (iConfig.getParameter < edm::InputTag > ("met"))), //
				minJetPtForHT_(iConfig.getParameter<double>("minJetPtForHT")), //
				prefix_(iConfig.getParameter < std::string > ("prefix")), //
				suffix_(iConfig.getParameter < std::string > ("suffix")), //
				channel_(iConfig.getParameter < std::string > ("channel")), //
				cleanedJets_(), //
				cleanedBJets_(), //
				signalElectrons_(), //
				signalMuons_(), //
				met_(), //
				lepton_p4_() {
	produces<double>(prefix_ + "HT" + suffix_);
	produces<double>(prefix_ + "ST" + suffix_);
	produces<double>(prefix_ + "M3" + suffix_);
	produces<double>(prefix_ + "Mbl" + suffix_);
	produces<double>(prefix_ + "anglebl" + suffix_);
	produces<double>(prefix_ + "MT" + suffix_);
	produces<double>(prefix_ + "WPT" + suffix_);

	produces<double>(prefix_ + "leptonEta" + suffix_);
	produces<double>(prefix_ + "leptonPt" + suffix_);

	produces<unsigned int>(prefix_ + "NJets" + suffix_);
	produces<unsigned int>(prefix_ + "NBJets" + suffix_);
}

void VariableProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	setupEventContent(iEvent, iSetup);

	std::auto_ptr<double> HT(new double(VariableProducer::HT(cleanedJets_, minJetPtForHT_)));
	std::auto_ptr<double> ST(new double(VariableProducer::ST(cleanedJets_, lepton_p4_, met_, minJetPtForHT_)));
	std::auto_ptr<double> M3(new double(VariableProducer::M3(cleanedJets_)));
	std::auto_ptr<double> Mbl(new double(-1));
	std::auto_ptr<double> anglebl(new double(-1));
	std::auto_ptr<double> MT(new double(VariableProducer::MT(lepton_p4_, met_)));
	std::auto_ptr<double> WPT(new double(VariableProducer::WPT(lepton_p4_, met_)));

	std::auto_ptr<double> leptonPt(new double(lepton_p4_.Pt()));
	std::auto_ptr<double> leptonEta(new double(lepton_p4_.Eta()));

	std::auto_ptr<unsigned int> nJets(new unsigned int(cleanedJets_.size()));
	std::auto_ptr<unsigned int> nBJets(new unsigned int(cleanedBJets_.size()));

	if (cleanedBJets_.size() > 0) {
		size_t closestBJetIndex = getClosestJet(lepton_p4_, cleanedBJets_);
		const pat::Jet& closestBJet = cleanedBJets_.at(closestBJetIndex);
		*Mbl = VariableProducer::M_bl(closestBJet, lepton_p4_);
		*anglebl = VariableProducer::angle_bl(closestBJet, lepton_p4_);
	}

	iEvent.put(HT, prefix_ + "HT" + suffix_);
	iEvent.put(ST, prefix_ + "ST" + suffix_);
	iEvent.put(M3, prefix_ + "M3" + suffix_);
	iEvent.put(Mbl, prefix_ + "Mbl" + suffix_);
	iEvent.put(anglebl, prefix_ + "anglebl" + suffix_);
	iEvent.put(MT, prefix_ + "MT" + suffix_);
	iEvent.put(WPT, prefix_ + "WPT" + suffix_);

	iEvent.put(leptonEta, prefix_ + "leptonEta" + suffix_);
	iEvent.put(leptonPt, prefix_ + "leptonPt" + suffix_);

	iEvent.put(nJets, prefix_ + "NJets" + suffix_);
	iEvent.put(nBJets, prefix_ + "NBJets" + suffix_);
}

void VariableProducer::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	LogDebug("NTP_VariableProducer") << "Setting up the event content";

	// jets
	LogDebug("NTP_VariableProducer") << "Getting clean jets";
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByToken(cleanedJetsToken_, jets);
	cleanedJets_ = *jets;

	LogDebug("NTP_VariableProducer") << "Getting clean b-jets";
	edm::Handle < pat::JetCollection > bjets;
	iEvent.getByToken(cleanedBJetsToken_, bjets);
	cleanedBJets_ = *bjets;

	// Electrons (for veto)
	LogDebug("NTP_VariableProducer") << "Getting signal electrons";
	edm::Handle < pat::ElectronCollection > electrons;
	iEvent.getByToken(signalElectronToken_, electrons);
	signalElectrons_ = *electrons;

	// veto muons
	LogDebug("NTP_VariableProducer") << "Getting signal muons";
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByToken(signalMuonToken_, muons);
	signalMuons_ = *muons;

	// veto mets
	LogDebug("NTP_VariableProducer") << "Getting MET";
	edm::Handle < pat::METCollection > mets;
	iEvent.getByToken(metToken_, mets);
	met_ = mets->front();

	if (channel_ == "electron") {
		const pat::Electron& lepton = signalElectrons_.front();
		lepton_p4_ = lepton.p4(); //.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy());
	} else if (channel_ == "muon") {
		const pat::Muon& lepton = signalMuons_.front();
		lepton_p4_ = lepton.p4(); //.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy());
	} else {
		edm::LogError("NTP_VariableProducer") << " Unknown channel: " << channel_;
	}
}

double VariableProducer::HT(const pat::JetCollection& jets, double minJetPt) {
	double ht(0);
	//Take ALL the jets!
	for (unsigned int index = 0; index < jets.size(); ++index) {
		if (jets.at(index).pt() > minJetPt)
			ht += jets.at(index).pt();
	}
	return ht;
}

double VariableProducer::ST(const pat::JetCollection& jets, const LorentzVector& lepton, const pat::MET& met,
		double minJetPt) {
	// ST = HT + MET + lepton pt
	double ht = VariableProducer::HT(jets, minJetPt);
	return ht + met.et() + lepton.Pt();
}

double VariableProducer::M3(const pat::JetCollection& jets) {
	double m3(0), max_pt(0);
	if (jets.size() >= 3) {
		for (unsigned int index1 = 0; index1 < jets.size() - 2; ++index1) {
			for (unsigned int index2 = index1 + 1; index2 < jets.size() - 1; ++index2) {
				for (unsigned int index3 = index2 + 1; index3 < jets.size(); ++index3) {
					const pat::Jet& jet1(jets.at(index1));
					const pat::Jet& jet2(jets.at(index2));
					const pat::Jet& jet3(jets.at(index3));

					const LorentzVector& m3Vector = jet1.p4() + jet2.p4() + jet3.p4();

					double currentPt = m3Vector.Pt();
					if (currentPt > max_pt) {
						max_pt = currentPt;
						m3 = m3Vector.M();
					}
				}
			}
		}
	}

	return m3;
}

double VariableProducer::M_bl(const pat::Jet& b_jet, const LorentzVector& lepton) {
	LorentzVector bl(lepton + b_jet.p4());

	return bl.M();
}

double VariableProducer::angle_bl(const pat::Jet& b_jet, const LorentzVector& lepton) {
	return angle(b_jet.p4(), lepton);
}

double VariableProducer::MT(const LorentzVector& lepton, const pat::MET& met) {
	double energySquared = pow(lepton.Et() + met.et(), 2);
	double momentumSquared = pow(lepton.Px() + met.px(), 2) + pow(lepton.Py() + met.py(), 2);
	double MTSquared = energySquared - momentumSquared;

	if (MTSquared > 0)
		return sqrt(MTSquared);
	else
		return -1;
}

double VariableProducer::WPT(const LorentzVector& lepton, const pat::MET& met) {
	LorentzVector W_boson(lepton + met.p4());
	return W_boson.Pt();
}
DEFINE_FWK_MODULE (VariableProducer);
}
