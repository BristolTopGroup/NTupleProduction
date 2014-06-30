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
	BTagWeight(int btagSystematicFactor, int lightJetSystematicFactor);

	double weight(unsigned int numberOf_b_Jets, unsigned int numberOf_c_Jets, unsigned int numberOf_udsg_Jets,
			double mean_bJetEfficiency, double mean_cFJetEfficiency, double mean_udsgJetEfficiency,
			double scaleFactor_b, double scaleFactor_c, double scaleFactor_udsg, unsigned int numberOfTags) const;
	std::vector<double> weights(const pat::JetCollection& jets, unsigned int numberOfBtags) const;

	std::vector<double> weights(unsigned int numberOf_b_Jets, unsigned int numberOf_c_Jets,
			unsigned int numberOf_udsg_Jets, double mean_bJetEfficiency, double mean_cFJetEfficiency,
			double mean_udsgJetEfficiency, double scaleFactor_b, double scaleFactor_c, double scaleFactor_udsg,
			unsigned int numberOfTags) const;

	std::vector<double> weights(double averageScaleFactor, unsigned int numberOfTags) const;

	void setNumberOfBtags(unsigned int min, unsigned int max);

	pat::JetCollection getBJets(const pat::JetCollection& jets) const;
	pat::JetCollection getCJets(const pat::JetCollection& jets) const;
	pat::JetCollection getUDSGJets(const pat::JetCollection& jets) const;

	bool filter(unsigned int t) const;

	double getAverageBScaleFactor(const pat::JetCollection&, std::string MCSampleTag, double uncertaintyFactor = 1.) const;
	double getBScaleFactor(const pat::Jet& jet, std::string MCSampleTag, double uncertaintyFactor = 1.) const;
	double getAverageBEfficiency() const;
	double getAverageCScaleFactor(const pat::JetCollection&, std::string MCSampleTag) const;
	double getCScaleFactor(const pat::Jet&, std::string MCSampleTag) const;
	double getAverageCEfficiency() const;
	double getAverageUDSGScaleFactor(const pat::JetCollection&, std::string MCSampleTag) const;
	double getUDSGScaleFactor(const pat::Jet&, std::string MCSampleTag) const;
	double getAverageUDSGEfficiency(const pat::JetCollection&) const;

	double getMeanUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const;
	double getMinUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const;
	double getMaxUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const;

	double getMeanUDSGEfficiency(double jetPT) const;
private:
	unsigned int minNumberOfTags_;
	unsigned int maxNumberOfTags_;
	int BJetSystematic_, LightJetSystematic_;

};

std::vector<double> BjetWeights(const pat::JetCollection& jets, unsigned int numberOfBtags, std::string MCSampleTag);
std::vector<double> BjetWeights(const pat::JetCollection& jets, unsigned int numberOfBtags, int btagSystematicFactor, int lightJetSystematicFactor, std::string MCSampleTag);
#endif

