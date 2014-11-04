#ifndef LQ_PatUtilities_h
#define LQ_PatUtilities_h

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"

reco::TrackRef pmcTrack(const pat::Muon& mu, int & refit_id);

reco::TrackRef tevOptimized(const reco::TrackRef& trackerTrack, const reco::TrackRef& gmrTrack,
		const reco::TrackRef& fmsTrack, const reco::TrackRef& pmrTrack, int & refit_id);

bool passesFilter(const edm::Event& event, const edm::InputTag filter);

bool triggerFired(const std::string& triggerWildCard, const HLTConfigProvider& hltConfig,
		const edm::TriggerResults& triggerResults);
unsigned int findTrigger(const std::string& triggerWildCard, const HLTConfigProvider& hltConfig);

double getRelativeIsolation(const pat::Electron& electron, double cone, double rho, bool isRealData,
		bool useDeltaBetaCorrections, bool useRhoActiveAreaCorrections);
double getRelativeIsolation(const pat::Muon& muon, double cone, bool useDeltaBetaCorrections);

double getSmearedJetPtScale(const pat::Jet& jet, int jet_smearing_systematic);

#endif 
