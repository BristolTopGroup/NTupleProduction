#ifndef MUONWEIGHT_H
#define MUONWEIGHT_H

#include "DataFormats/PatCandidates/interface/Muon.h"
#include <TH2F.h>
#include <TH3F.h>

/**
 * Modified by Emyr Clement
 */

class MuonWeight {
public:
	MuonWeight();
	MuonWeight(int muonSystematicFactor);

	double weight(const pat::Muon& muon, TH2F* muonIdIsoScaleFactorsHistogram, TH3F* muonTriggerScaleFactorsHistogram, int Systematic, std::string MCSampleTag ) const;

	double getTriggerScaleFactor( const pat::Muon&, TH3F* muonTriggerScaleFactorsHistogram, std::string MCSampleTag ) const;
	double getIDScaleFactor( const pat::Muon&, TH2F* muonIdIsoScaleFactorsHistogram, std::string MCSampleTag ) const;

private:
	int Systematic_;

};

std::vector<double> MuonWeights(const pat::MuonCollection& muon, TH2F* muonIdIsoScaleFactorsHistogram, TH3F* muonTriggerScaleFactorsHistogram, int muonSystematicFactor, std::string MCSampleTag);
#endif

