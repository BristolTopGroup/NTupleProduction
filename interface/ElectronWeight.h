#ifndef ELECTRONWEIGHT_H
#define ELECTRONWEIGHT_H

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include <TH2F.h>
#include <TEfficiency.h>

/**
 * Modified by Emyr Clement
 */

class ElectronWeight {
public:
	ElectronWeight();
	ElectronWeight(int electronSystematicFactor);

	double weight(const pat::Electron& electron, const pat::Jet& jet,  TH2F* electronIdIsoScaleFactorsHistogram, TEfficiency* electronTriggerEfficiencyHistogram, TH1F* hadronLegTriggerHistogram, int Systematic, std::string MCSampleTag ) const;

private:
	int Systematic_;

	double getTriggerScaleFactor( const pat::Electron&, TEfficiency* electronTriggerEfficiencyHistogram, std::string MCSampleTag ) const;
	double getIDScaleFactor( const pat::Electron&, TH2F* electronIdIsoScaleFactorsHistogram, std::string MCSampleTag ) const;
	double getHadronLegTriggerEfficiency( const pat::Jet&, TH1F* hadronLegTriggerHistogram, std::string MCSampleTag ) const;
};

std::vector<double> ElectronWeights(const pat::ElectronCollection& electron,  const pat::Jet& jet, TH2F* electronIdIsoScaleFactorsHistogram, TEfficiency* electronTriggerEfficiencyHistogram, TH1F* hadronLegTriggerHistogram, int electronSystematicFactor, std::string MCSampleTag);
#endif

