#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"

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

bool passesFilter(const edm::Event& event, const edm::InputTag filter) {
	bool result(false);
	edm::Handle<bool> filterResult;
	event.getByLabel(filter, filterResult);
	if (filterResult.isValid()) {
		edm::LogInfo("PatUtilities_Filter") << "Successfully obtained " << filter;
		result = *filterResult;
	} else
		edm::LogError("PatUtilities_Filter_Error") << "Error! Can't get the product " << filter;

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
	if (abs(electron.superCluster()->eta()) > 1.479) {
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

	if (useDeltaBetaCorrections)
		return relIsodb;
	if (useRhoActiveAreaCorrections)
		return relIsorho;

	return relIso;
}

double getRelativeIsolation(const pat::Muon& muon, double cone, bool useDeltaBetaCorrections) {
	const double chIso = muon.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(cone).first;
	const double nhIso = muon.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(cone).first;
	const double phIso = muon.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(cone).first;

	const double puChIso = muon.isoDeposit(pat::PfPUChargedHadronIso)->depositAndCountWithin(0.4).first;

	const double relIso = (chIso + nhIso + phIso) / muon.pt();
	const double relIsodb = (chIso + max(0.0, nhIso + phIso - 0.5 * puChIso)) / muon.pt();

	if (useDeltaBetaCorrections)
		return relIsodb;

	return relIso;
}
