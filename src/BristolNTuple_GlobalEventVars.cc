#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GlobalEventVars.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

BristolNTuple_GlobalEventVars::BristolNTuple_GlobalEventVars(const edm::ParameterSet& iConfig) :
	jetInputTag(iConfig.getParameter < edm::InputTag > ("jetInputTag")), //
	leptonInputTag(iConfig.getParameter < edm::InputTag > ("signalLeptonInputTag")), //
	leptonIndexInputTag(iConfig.getParameter < edm::InputTag > ("signalLeptonIndexInputTag")), //
	metInputTag(iConfig.getParameter < edm::InputTag > ("metInputTag")), //
	prefix(iConfig.getParameter < std::string > ("Prefix")), //
	suffix(iConfig.getParameter < std::string > ("Suffix")), //
	channel(iConfig.getParameter < std::string > ("Channel"))
{
	produces<double>(prefix + "HT" + suffix);
	produces<double>(prefix + "ST" + suffix);
	produces<double>(prefix + "M3" + suffix);
	produces<double>(prefix + "Mbl" + suffix);
	produces<double>(prefix + "anglebl" + suffix);
	produces<double>(prefix + "MT" + suffix);
	produces<double>(prefix + "WPT" + suffix);
	produces<unsigned int>(prefix + "signalLeptonIndex" + suffix);
	produces<unsigned int>(prefix + "numberOfBTags" + suffix);
}

void BristolNTuple_GlobalEventVars::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle < pat::JetCollection > jets;
    iEvent.getByLabel(jetInputTag, jets);

    if (!jets.isValid())
      edm::LogError("BristolNTuple_GlobalEventVarsExtraError") << "Error! Can't get the product " << jetInputTag;

    TLorentzVector signalLepton;

    if ( channel=="EPlusJets" ) {
        edm::Handle < std::vector<pat::Electron> > leptons;
        iEvent.getByLabel(leptonInputTag, leptons);
        if (!leptons.isValid())
              edm::LogError("BristolNTuple_GlobalEventVarsExtraError") << "Error! Can't get the product " << leptonInputTag;

        pat::Electron lepton = leptons->at(0);
        signalLepton.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy());
    }
    else if ( channel=="MuPlusJets" ) {
        edm::Handle < std::vector<pat::Muon> > leptons;
        iEvent.getByLabel(leptonInputTag, leptons);
        if (!leptons.isValid())
              edm::LogError("BristolNTuple_GlobalEventVarsExtraError") << "Error! Can't get the product " << leptonInputTag;

        pat::Muon lepton = leptons->at(0);
        signalLepton.SetPxPyPzE(lepton.px(), lepton.py(), lepton.pz(), lepton.energy());

    }
    else {
    	std::cout << "Properly handle this error" << std::endl;
    	std::cout << "Channel : " << channel.c_str() << std::endl;
    }

    edm::Handle < unsigned int> signalLeptonIndex;
    iEvent.getByLabel( leptonIndexInputTag, signalLeptonIndex );

	edm::Handle < std::vector<pat::MET> > mets;
	iEvent.getByLabel(metInputTag, mets);

	if (!mets.isValid())
		edm::LogError("BristolNTuple_METExtraError") << "Error! Can't get the product " << metInputTag;

	const pat::MET patMET(mets->at(0));

    std::auto_ptr<double> HT(new double( BristolNTuple_GlobalEventVars::HT(*jets) ));
    std::auto_ptr<double> ST(new double( BristolNTuple_GlobalEventVars::ST(*jets, signalLepton, patMET) ));
    std::auto_ptr<double> M3(new double( BristolNTuple_GlobalEventVars::M3(*jets) ));
    std::auto_ptr<double> MT(new double( BristolNTuple_GlobalEventVars::MT(signalLepton, patMET) ));
    std::auto_ptr<double> WPT(new double( BristolNTuple_GlobalEventVars::WPT(signalLepton, patMET) ));

    // Get subset of jets that are tagged as b jets
    std::vector<const pat::Jet*> b_jets;
	for (unsigned int jetIndex = 0; jetIndex < jets->size(); ++jetIndex) {
		if ( jets->at(jetIndex).bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679 ) {
			b_jets.push_back( &jets->at(jetIndex) );
		}
	}

    std::auto_ptr<double> Mbl(new double(-1));
    std::auto_ptr<double> anglebl(new double(-1));

    // Get the b jet closest to the lepton
	if (b_jets.size() != 0) {
		unsigned int closestIndex = BristolNTuple_GlobalEventVars::getClosestBJet( signalLepton, b_jets );
		const pat::Jet* closestBJet = b_jets.at(closestIndex);

		*Mbl = BristolNTuple_GlobalEventVars::M_bl(closestBJet, signalLepton);
		*anglebl = BristolNTuple_GlobalEventVars::angle_bl(closestBJet, signalLepton);
	}

	iEvent.put(HT, prefix + "HT" + suffix);
	iEvent.put(ST, prefix + "ST" + suffix);
	iEvent.put(M3, prefix + "M3" + suffix);
	iEvent.put(Mbl, prefix + "Mbl" + suffix);
	iEvent.put(anglebl, prefix + "anglebl" + suffix);
	iEvent.put(MT, prefix + "MT" + suffix);
	iEvent.put(WPT, prefix + "WPT" + suffix);

	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(b_jets.size())),prefix + "numberOfBTags" + suffix);
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(*signalLeptonIndex)),prefix + "signalLeptonIndex" + suffix);

}

double BristolNTuple_GlobalEventVars::HT(const pat::JetCollection& jets) {
	double ht(0);
	//Take ALL the jets!
	for (unsigned int index = 0; index < jets.size(); ++index) {
		if(jets.at(index).pt() > 20)
			ht += jets.at(index).pt();
	}
	return ht;
}

double BristolNTuple_GlobalEventVars::ST(const pat::JetCollection& jets, const TLorentzVector& lepton, const pat::MET& met) {
	// ST = HT + MET + lepton pt
	double ht = BristolNTuple_GlobalEventVars::HT(jets);
	return ht + met.et() + lepton.Pt();
}

double BristolNTuple_GlobalEventVars::M3(const pat::JetCollection& jets) {
	double m3(0), max_pt(0);
	if (jets.size() >= 3) {
		for (unsigned int index1 = 0; index1 < jets.size() - 2; ++index1) {
			for (unsigned int index2 = index1 + 1; index2 < jets.size() - 1;
					++index2) {
				for (unsigned int index3 = index2 + 1; index3 < jets.size();
						++index3) {
					TLorentzVector jet1( jets.at(index1).px(), jets.at(index1).py(), jets.at(index1).pz(), jets.at(index1).energy() );
					TLorentzVector jet2( jets.at(index2).px(), jets.at(index2).py(), jets.at(index2).pz(), jets.at(index2).energy() );
					TLorentzVector jet3( jets.at(index3).px(), jets.at(index3).py(), jets.at(index3).pz(), jets.at(index3).energy() );

					TLorentzVector m3Vector(jet1 + jet2 + jet3);
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

double BristolNTuple_GlobalEventVars::M_bl(const pat::Jet* b_jet, const TLorentzVector& lepton ) {
	double m_bl(0.);
	TLorentzVector b( b_jet->px(), b_jet->py(), b_jet->pz(), b_jet->energy() );
	TLorentzVector bl( lepton + b );

	m_bl = bl.M();
	return m_bl;
}

double BristolNTuple_GlobalEventVars::angle_bl(const pat::Jet* b_jet, const TLorentzVector& lepton) {
	double angle(-1);
	TLorentzVector b( b_jet->px(), b_jet->py(), b_jet->pz(), b_jet->energy() );
	angle = b.Angle(lepton.Vect());
	return angle;
}

unsigned int BristolNTuple_GlobalEventVars::getClosestBJet( const TLorentzVector& lepton, const std::vector<const pat::Jet*> b_jets) {
	// find closest b_jet
	double closestDR = 9999;
	unsigned int closestIndex = 9999;
	for ( unsigned int index = 0; index < b_jets.size(); index++ ) {
		double DR = deltaR( lepton.Eta(), lepton.Phi(), b_jets.at(index)->eta(), b_jets.at(index)->phi() );
		if ( DR < closestDR ) {
			closestDR = DR;
			closestIndex = index;
		}
	}
	return closestIndex;
}



double BristolNTuple_GlobalEventVars::MT(const TLorentzVector& lepton, const pat::MET& met) {
	double energySquared = pow(lepton.Et() + met.et(), 2);
	double momentumSquared = pow(lepton.Px() + met.px(), 2) + pow(lepton.Py() + met.py(), 2);
	double MTSquared = energySquared - momentumSquared;

	if (MTSquared > 0)
		return sqrt(MTSquared);
	else
		return -1;
}

double BristolNTuple_GlobalEventVars::WPT(const TLorentzVector& lepton, const pat::MET& met) {
	TLorentzVector m( met.px(), met.py(), met.pz(), met.energy() );
	TLorentzVector W_boson(lepton + m );
	return W_boson.Pt();
}
