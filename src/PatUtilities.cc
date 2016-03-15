#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"

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

double getRelativeIsolation(const pat::Electron& electron, double cone, double rho, bool isRealData, bool useDeltaBetaCorrections,
		bool useRhoActiveAreaCorrections) {
	//code from: https://twiki.cern.ch/twiki/bin/view/CMS/PfIsolation
	float AEff = 0.00;
	//so far this is only for 0.3. 0.4 is available but not 0.5

// 	  std::cout << "ElectronEffectiveArea::kEleEAData2011: " << ElectronEffectiveArea::kEleEAData2011 << std::endl;
//        std::cout << "ElectronEffectiveArea::kEleEAData2012: " << ElectronEffectiveArea::kEleEAData2012<< std::endl;

//        std::cout << "ElectronEffectiveArea::kEleEAFall1MC: " << ElectronEffectiveArea::kEleEAFall11MC << std::endl;
//        std::cout << "ElectronEffectiveArea::kEleEASummer12MC: " << ElectronEffectiveArea::kEleEASummer12MC<< std::endl;

        if (isRealData) {
		AEff = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03,
				electron.superCluster()->eta(), ElectronEffectiveArea::kEleEAData2012);
        } else {
		AEff = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03,
				electron.superCluster()->eta(), ElectronEffectiveArea::kEleEAData2012);
	}

	AbsVetos vetos_ch;
	AbsVetos vetos_nh;
	AbsVetos vetos_ph;

	Direction Dir = Direction(electron.superCluster()->eta(), electron.superCluster()->phi());

	//pf isolation veto setup EGM recommendation
	if (fabs(electron.superCluster()->eta()) > 1.479) {
		vetos_ch.push_back(new ConeVeto(Dir, 0.015));
		vetos_ph.push_back(new ConeVeto(Dir, 0.08));
	}

	const double chIso = electron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(cone, vetos_ch).first;
	const double nhIso = electron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(cone, vetos_nh).first;
	const double phIso = electron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(cone, vetos_ph).first;

	const double puChIso = electron.isoDeposit(pat::PfPUChargedHadronIso)->depositAndCountWithin(cone, vetos_ch).first;

	const double relIso = (chIso + nhIso + phIso) / electron.pt();
	const double relIsodb = (chIso + max(0.0, nhIso + phIso - 0.5 * puChIso)) / electron.pt();
	const double relIsorho = (chIso + max(0.0, nhIso + phIso - rho * AEff)) / electron.pt();
	
	if (useRhoActiveAreaCorrections)
		return relIsorho;
	
	if (useDeltaBetaCorrections)
		return relIsodb;
	

	return relIso;
}

double getRelativeIsolation(const pat::Muon& muon, double cone, bool useDeltaBetaCorrections) {
	double chIso = 0;
	double nhIso = 0; 
	double phIso = 0;
	double puChIso = 0;
	
	if(cone==0.3){
 	chIso = muon.pfIsolationR03().sumChargedHadronPt;
 	nhIso = muon.pfIsolationR03().sumNeutralHadronEt;
 	phIso = muon.pfIsolationR03().sumPhotonEt;
	puChIso = muon.pfIsolationR03().sumPUPt;
	}else{
	chIso = muon.pfIsolationR04().sumChargedHadronPt;
 	nhIso = muon.pfIsolationR04().sumNeutralHadronEt;
 	phIso = muon.pfIsolationR04().sumPhotonEt;
	puChIso = muon.pfIsolationR04().sumPUPt;
	
	}
	
	
	const double relIso = (chIso + nhIso + phIso) / muon.pt();
	const double relIsodb = (chIso + max(0.0, nhIso + phIso - 0.5 * puChIso)) / muon.pt();

	if (useDeltaBetaCorrections)
		return relIsodb;

	return relIso;
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



