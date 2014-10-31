#ifndef BTAGWEIGHT_H
#define BTAGWEIGHT_H

#include "DataFormats/PatCandidates/interface/Jet.h"
/**
 * Original by Andrea Rizzi
 * Modified by Lukasz Kreczko
 */

class BTagWeight {
public:
	BTagWeight();
	BTagWeight(int btagSystematicFactor);

	double weight(const pat::JetCollection& jets, int BTagSystematic, std::string MCSampleTag ) const;

	void setNumberOfBtags(unsigned int min, unsigned int max);

	bool filter( unsigned int t ) const;

	double getEfficiency( const unsigned int, const pat::Jet&, std::string MCSampleTag ) const;
	std::vector<double> getScaleFactor( const double, const pat::Jet&, std::string MCSampleTag ) const;

	std::vector<double> getBScaleFactor( const pat::Jet&, std::string MCSampleTag, double uncertaintyFactor = 1. ) const;
	double getBEfficiency( const pat::Jet&, std::string MCSampleTag ) const;
	std::vector<double> getCScaleFactor( const pat::Jet&, std::string MCSampleTag ) const;
	double getCEfficiency( const pat::Jet&, std::string MCSampleTag ) const;
	std::vector<double> getUDSGScaleFactor( const pat::Jet&, std::string MCSampleTag ) const;
	double getUDSGEfficiency( const pat::Jet&, std::string MCSampleTag ) const;


	double getMeanUDSGScaleFactor( double jetPT, double jetEta, std::string MCSampleTag ) const;
	double getMinUDSGScaleFactor( double jetPT, double jetEta, std::string MCSampleTag ) const;
	double getMaxUDSGScaleFactor( double jetPT, double jetEta, std::string MCSampleTag ) const;

	double getMeanUDSGEfficiency(double jetPT) const;
private:
	unsigned int minNumberOfTags_;
	unsigned int maxNumberOfTags_;
	int BJetSystematic_, LightJetSystematic_;

};

std::vector<double> BjetWeights(const pat::JetCollection& jets, unsigned int numberOfBtags, std::string MCSampleTag);
std::vector<double> BjetWeights(const pat::JetCollection& jets, unsigned int numberOfBtags, int btagSystematicFactor, std::string MCSampleTag);
#endif

