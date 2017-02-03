#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "TLorentzVector.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;


reco::TrackRef pmcTrack(const pat::Muon& mu, int & refit_id) {
	return tevOptimized(mu.innerTrack(), mu.globalTrack(), mu.tpfmsMuon(), mu.pickyMuon(), refit_id);
}

reco::TrackRef tevOptimized(const reco::TrackRef& trackerTrack, const reco::TrackRef& gmrTrack,
		const reco::TrackRef& fmsTrack, const reco::TrackRef& pmrTrack, int & refit_id) {
	const reco::TrackRef refit[4] = { trackerTrack, gmrTrack, fmsTrack, pmrTrack };

	double prob[4] = { 0. };
	int chosen = 3;

	for (unsigned int i = 0; i < 4; ++i)
		if (refit[i].isNonnull() && refit[i]->numberOfValidHits())
			prob[i] = muon::trackProbability(refit[i]);

	if (prob[3] == 0.) {
		if (prob[2] > 0.)
			chosen = 2;
		else if (prob[1] > 0.)
			chosen = 1;
		else if (prob[0] > 0.)
			chosen = 0;
	}

	if (prob[0] > 0. && prob[3] > 0. && prob[3] - prob[0] > 30.)
		chosen = 0;
	if (prob[2] > 0. && prob[chosen] - prob[2] > 0.)
		chosen = 2;

	refit_id = chosen;
	return refit[chosen];
}

bool passesFilter(const edm::Event& event, const edm::EDGetTokenT<bool> filter) {
	bool result(false);

	edm::Handle<bool> filterResult;
	event.getByToken(filter, filterResult);
	if (filterResult.isValid()) {
		// edm::LogInfo("PatUtilities_Filter") << "Successfully obtained " << filter;
		result = *filterResult;
	} 
	// else
	// 	edm::LogError("PatUtilities_Filter_Error") << "Error! Can't get the product " << filter;

	return result;
}

bool triggerFired(const std::string& triggerWildCard, const HLTConfigProvider& hltConfig,
		const edm::TriggerResults& triggerResults) {
	bool fired(false);
	unsigned int index = findTrigger(triggerWildCard, hltConfig);

	if (index < triggerResults.size()) {
		if (triggerResults.accept(index))
			fired = true;
	} else {
		edm::LogInfo("PATUtilities") << "Requested HLT path \"" << (triggerWildCard) << "\" does not exist";
	}
	return fired;
}

unsigned int findTrigger(const std::string& triggerWildCard, const HLTConfigProvider& hltConfig) {
	const std::vector<std::string>& triggers = hltConfig.triggerNames();
	unsigned int found = 9999;

	size_t length = triggerWildCard.size();
	for (unsigned int index = 0; index < triggers.size(); ++index) {
		if (length <= triggers[index].size() && triggerWildCard == triggers[index].substr(0, length)) {
			found = index;
			break;
		}
	}

	return found;
}

double getSmearedJetPtScale(const pat::Jet& jet, int jet_smearing_systematic) {
	// Get the jet energy resolution scale factors, depending on the jet eta, from 
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution#Recommendations_for_7_and_8_TeV
	
				
	//Jeson's smeary code:
	double scaleFactor(0.);
	if (fabs(jet.eta()) >= 0.0 && fabs(jet.eta()) < 0.5) {
		switch (jet_smearing_systematic) {
			case -1:
				scaleFactor = 0.990;
				break;
			case 1:
				scaleFactor = 1.115;
				break;
			default:
				scaleFactor = 1.052;
		}
	}
	if (fabs(jet.eta()) >= 0.5 && fabs(jet.eta()) < 1.1) {
		switch (jet_smearing_systematic) {
			case -1:
				scaleFactor = 1.001;
				break;
			case 1:
				scaleFactor = 1.114;
				break;
			default:
				scaleFactor = 1.057;
		}
	}
	if (fabs(jet.eta()) >= 1.1 && fabs(jet.eta()) < 1.7) {
		switch (jet_smearing_systematic) {
			case -1:
				scaleFactor = 1.032;
				break;
			case 1:
				scaleFactor = 1.161;
				break;
			default:
				scaleFactor = 1.096;
		}
	}
	if (fabs(jet.eta()) >= 1.7 && fabs(jet.eta()) < 2.3) {
		switch (jet_smearing_systematic) {
			case -1:
				scaleFactor = 1.042;
				break;
			case 1:
				scaleFactor = 1.228;
				break;
			default:
				scaleFactor = 1.134;
		}
	}
	if (fabs(jet.eta()) >= 2.3 && fabs(jet.eta()) < 5.0) {
		switch (jet_smearing_systematic) {
			case -1:
				scaleFactor = 1.089;
				break;
			case 1:
				scaleFactor = 1.488;
				break;
			default:
				scaleFactor = 1.288;
		}
	}

	//use raw scaleFactors from above to calculate the final factors to apply
	double matchedGeneratedJetpt = jet.pt();
	if(jet.genJet()){
		if ( jet.genJet()->energy() != 0 ) { // Check done in Analysis Tools
			matchedGeneratedJetpt = jet.genJet()->pt();
		}
	}
	double jetPt = jet.pt();
	double factor = 1-scaleFactor;
	double deltaPt = factor * (jetPt - matchedGeneratedJetpt);
	double ptScale = std::max(0.0, ((jetPt + deltaPt)/jetPt));

	return ptScale;

}

pat::JetCollection applyNewJec( pat::JetCollection jets, const JetCorrector* corrector, edm::Event& iEvent, const edm::EventSetup& iSetup ) {
	pat::JetCollection newJets;

	for (unsigned index = 0; index < jets.size(); ++index) {
		const pat::Jet jet = jets.at(index);
		float JEC = getJECForJet( jet, corrector, iEvent, iSetup);
		pat::Jet newJet( jet );
		newJet.setP4( jet.correctedJet("Uncorrected").p4() * JEC );
		newJets.push_back( newJet );
	}

	return newJets;
}

float getJECForJet(const pat::Jet jet, const JetCorrector* corrector, edm::Event& iEvent, const edm::EventSetup& iSetup ) {
	return corrector->correction( jet.correctedJet("Uncorrected"), iEvent, iSetup );
}


namespace ntp {
namespace utils {
double ht(const pat::JetCollection& jets)
{
  double result = 0;
  for (auto jet : jets) {
    result += jet.pt();
  }
  return result;
}

double st(const pat::JetCollection& jets, const pat::MET& met, const reco::Candidate* lepton)
{
  return ht(jets) + met.pt() + lepton->pt();
}

double wpt(const pat::MET& met, const reco::Candidate* lepton)
{
  return sqrt(pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2));
}

double mt(const pat::MET& met, const reco::Candidate* lepton)
{
  double energy_squared = pow(lepton->et() + met.pt(), 2);
  double momentum_squared = pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2);
  double MT_squared = energy_squared - momentum_squared;

  if (MT_squared > 0)
    return sqrt(MT_squared);
  else
    return -1;
}

double m3(const pat::JetCollection& jets)
{
  double m3(-1), max_pt(0);
  if (jets.size() >= 3) {
    for (unsigned int index1 = 0; index1 < jets.size() - 2; ++index1) {
      for (unsigned int index2 = index1 + 1; index2 < jets.size() - 1; ++index2) {
        for (unsigned int index3 = index2 + 1; index3 < jets.size(); ++index3) {
          TLorentzVector jet1(jets.at(index1).px(), jets.at(index1).py(), jets.at(index1).pz(),
              jets.at(index1).energy());
          TLorentzVector jet2(jets.at(index2).px(), jets.at(index2).py(), jets.at(index2).pz(),
              jets.at(index2).energy());
          TLorentzVector jet3(jets.at(index3).px(), jets.at(index3).py(), jets.at(index3).pz(),
              jets.at(index3).energy());

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

double angle_bl(const pat::JetCollection& jets, const reco::Candidate* lepton)
{
  double angle(-1);
  const pat::Jet closestJet(getClosestJet(jets, lepton));

  TLorentzVector b(closestJet.px(), closestJet.py(), closestJet.pz(), closestJet.energy());
  TLorentzVector l(lepton->px(), lepton->py(), lepton->pz(), lepton->energy());

  angle = b.Angle(l.Vect());

  return angle;
}

pat::Jet getClosestJet(const pat::JetCollection& jets, const reco::Candidate* lepton)
{
  double closestDR = 9999;
  pat::Jet closestJet;

  for (auto jet : jets) {
    double DR = deltaR(lepton->eta(), lepton->phi(), jet.eta(), jet.phi());
    if (DR < closestDR) {
      closestDR = DR;
      closestJet = pat::Jet(jet);
    }
  }

  return closestJet;
}

double m_bl(const pat::JetCollection& jets, const reco::Candidate* lepton)
{
  double mass(-1);
  const pat::Jet closestJet(getClosestJet(jets, lepton));

  TLorentzVector b(closestJet.px(), closestJet.py(), closestJet.pz(), closestJet.energy());
  TLorentzVector l(lepton->px(), lepton->py(), lepton->pz(), lepton->energy());

  mass = (b + l).M();

  return mass;
}
}
}



