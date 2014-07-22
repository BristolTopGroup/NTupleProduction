#include "BristolAnalysis/NTupleTools/interface/BTagWeight.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

#include <functional>
#include <numeric>
#include <boost/scoped_ptr.hpp>
#include <boost/array.hpp>

using namespace pat;

//Btag weights using this method: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagWeight
//And SFs taken from here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG#2012_Data_and_MC_Moriond13_presc

std::vector<double> BjetWeights(const JetCollection& jets, unsigned int numberOfBtags, std::string MCSampleTag) {
	boost::scoped_ptr < BTagWeight > btagWeight(new BTagWeight());
	//get b-jets
	const JetCollection bjets(btagWeight->getBJets(jets));
	//get c-jets
	const JetCollection cjets(btagWeight->getCJets(jets));
	//get udsg jets
	const JetCollection udsgjets(btagWeight->getUDSGJets(jets));

	//get mean scale factors
	double SF_b = btagWeight->getAverageBScaleFactor(bjets, MCSampleTag);
	double SF_c = btagWeight->getAverageCScaleFactor(cjets, MCSampleTag);
	double SF_udsg = btagWeight->getAverageUDSGScaleFactor(udsgjets, MCSampleTag);
	//get mean efficiencies
	double mean_bJetEfficiency = btagWeight->getAverageBEfficiency();
	double mean_cJetEfficiency = btagWeight->getAverageCEfficiency();
	double mean_udsgJetEfficiency = btagWeight->getAverageUDSGEfficiency(udsgjets);

	std::vector<double> event_weights;
	for (unsigned int nTag = 0; nTag <= numberOfBtags; ++nTag) { // >= 4 is our last b-tag bin!
		btagWeight->setNumberOfBtags(nTag, 20);
		double event_weight = btagWeight->weight(bjets.size(), cjets.size(), udsgjets.size(), mean_bJetEfficiency,
				mean_cJetEfficiency, mean_udsgJetEfficiency, SF_b, SF_c, SF_udsg, numberOfBtags);
		event_weights.push_back(event_weight);
	}
	//all weights are inclusive. To get the weight for exclusive N b-tags ones has to subtract:
	for (unsigned int nTag = 0; nTag < numberOfBtags; ++nTag) {
		// w(N b-tags) = w(>= N) - w(>= N+1)
		event_weights.at(nTag) = event_weights.at(nTag) - event_weights.at(nTag + 1);
		//last weight, >= numberOfBjets jets, stays inclusive
	}
	return event_weights;
}

//this can be done shorter if you introduce a function which passes the btagWeight
std::vector<double> BjetWeights(const JetCollection& jets, unsigned int numberOfBtags, int btagSystematicFactor,
		int lightJetSystematicFactor, std::string MCSampleTag) {
	boost::scoped_ptr < BTagWeight > btagWeight(new BTagWeight(btagSystematicFactor, lightJetSystematicFactor));
	//get b-jets
	const JetCollection bjets(btagWeight->getBJets(jets));
	//get c-jets
	const JetCollection cjets(btagWeight->getCJets(jets));
	//get udsg jets
	const JetCollection udsgjets(btagWeight->getUDSGJets(jets));

	//get mean scale factors
	double SF_b = btagWeight->getAverageBScaleFactor(bjets, MCSampleTag);
	double SF_c = btagWeight->getAverageCScaleFactor(cjets, MCSampleTag);
	double SF_udsg = btagWeight->getAverageUDSGScaleFactor(udsgjets, MCSampleTag);
	//get mean efficiencies
	double mean_bJetEfficiency = btagWeight->getAverageBEfficiency();
	double mean_cJetEfficiency = btagWeight->getAverageCEfficiency();
	double mean_udsgJetEfficiency = btagWeight->getAverageUDSGEfficiency(udsgjets);

	std::vector<double> event_weights;
	for (unsigned int nTag = 0; nTag <= numberOfBtags; ++nTag) { // >= 4 is our last b-tag bin!
		btagWeight->setNumberOfBtags(nTag, 20);
		double event_weight = btagWeight->weight(bjets.size(), cjets.size(), udsgjets.size(), mean_bJetEfficiency,
				mean_cJetEfficiency, mean_udsgJetEfficiency, SF_b, SF_c, SF_udsg, numberOfBtags);
		event_weights.push_back(event_weight);
	}
	//all weights are inclusive. To get the weight for exclusive N b-tags ones has to subtract:
	for (unsigned int nTag = 0; nTag < numberOfBtags; ++nTag) {
		// w(N b-tags) = w(>= N) - w(>= N+1)
		event_weights.at(nTag) = event_weights.at(nTag) - event_weights.at(nTag + 1);
		//last weight, >= numberOfBjets jets, stays inclusive
	}
	return event_weights;
}

unsigned int fact(unsigned int n) {
	if (n < 1)
		return 1;
	unsigned int r = 1;
	for (unsigned int i = n; i > 1; i--)
		r *= i;

	return r;
}

unsigned int comb(unsigned int n, unsigned int k) {
	return fact(n) / fact(k) / fact(n - k);
}

BTagWeight::BTagWeight() :
		minNumberOfTags_(0), //
		maxNumberOfTags_(0), BJetSystematic_(0), //
		LightJetSystematic_(0) {

}

BTagWeight::BTagWeight(int btagSystematicFactor, int lightJetSystematicFactor) :
		minNumberOfTags_(0), //
		maxNumberOfTags_(0), BJetSystematic_(btagSystematicFactor), //
		LightJetSystematic_(lightJetSystematicFactor) {

}

bool BTagWeight::filter(unsigned int numberOfTags) const {
	return (numberOfTags >= minNumberOfTags_ && numberOfTags <= maxNumberOfTags_);
}

double BTagWeight::weight(unsigned int numberOf_b_Jets, unsigned int numberOf_c_Jets, unsigned int numberOf_udsg_Jets,
		double mean_bJetEfficiency, double mean_cJetEfficiency, double mean_udsgJetEfficiency, double scaleFactor_b,
		double scaleFactor_c, double scaleFactor_udsg, unsigned int numberOfTags) const {
	if (!filter(numberOfTags)) {
		return 0;
	}

	double probabilityMC = 0;
	double probabilityData = 0;
	for (unsigned int b_index = 0; b_index <= numberOf_b_Jets; ++b_index)
		for (unsigned int c_index = 0; c_index <= numberOf_c_Jets; ++c_index)
			for (unsigned int udsg_index = 0; udsg_index <= numberOf_udsg_Jets; ++udsg_index) {
				unsigned int t = b_index + c_index + udsg_index;
				if (!filter(t))
					continue;

				// how many equivalent ways
				unsigned int totalCombinations = comb(numberOf_b_Jets, b_index) * comb(numberOf_c_Jets, c_index)
						* comb(numberOf_udsg_Jets, udsg_index);

				probabilityMC += 1. * totalCombinations * pow(mean_bJetEfficiency, b_index)
						* pow(1. - mean_bJetEfficiency, numberOf_b_Jets - b_index) * pow(mean_cJetEfficiency, c_index)
						* pow(1. - mean_cJetEfficiency, numberOf_c_Jets - c_index)
						* pow(mean_udsgJetEfficiency, udsg_index)
						* pow(1. - mean_udsgJetEfficiency, numberOf_udsg_Jets - udsg_index);

				probabilityData += 1. * totalCombinations * pow(mean_bJetEfficiency * scaleFactor_b, b_index)
						* pow(1. - mean_bJetEfficiency * scaleFactor_b, numberOf_b_Jets - b_index)
						* pow(mean_cJetEfficiency * scaleFactor_c, c_index)
						* pow(1. - mean_cJetEfficiency * scaleFactor_c, numberOf_c_Jets - c_index)
						* pow(mean_udsgJetEfficiency * scaleFactor_udsg, udsg_index)
						* pow(1. - mean_udsgJetEfficiency * scaleFactor_udsg, numberOf_udsg_Jets - udsg_index);
			}
	if (probabilityMC == 0)
		return 0;
	return probabilityData / probabilityMC;
}

//std::vector<double> BTagWeight::weights(unsigned int numberOf_b_Jets, unsigned int numberOf_c_Jets,
//		unsigned int numberOf_udsg_Jets, double mean_bJetEfficiency, double mean_cJetEfficiency,
//		double mean_udsgJetEfficiency, double scaleFactor_b, double scaleFactor_c, double scaleFactor_udsg,
//		unsigned int numberOfTags) const {
//
//	std::vector<double> event_weights;
//	for (unsigned index = 0; index <= numberOf_b_Jets + numberOf_c_Jets + numberOf_udsg_Jets; ++index) {
//		event_weights.push_back(0);
//	}
//	if (!filter(numberOfTags)) {
//		return event_weights;
//	}
//
//	for (unsigned int b_index = 0; b_index <= numberOf_b_Jets; ++b_index)
//		for (unsigned int c_index = 0; c_index <= numberOf_c_Jets; ++c_index)
//			for (unsigned int udsg_index = 0; udsg_index <= numberOf_udsg_Jets; ++udsg_index) {
//				unsigned int t = b_index + c_index + udsg_index;
////				if (!filter(t))
////					continue;
//				double probabilityMC = 0;
//				double probabilityData = 0;
//				// how many equivalent ways
////				unsigned int totalCombinations = comb(numberOf_b_Jets, b_index) * comb(numberOf_c_Jets, c_index)
////						* comb(numberOf_udsg_Jets, udsg_index);
//
//				probabilityMC = pow(mean_bJetEfficiency, b_index)
//						* pow(1. - mean_bJetEfficiency, numberOf_b_Jets - b_index) * pow(mean_cJetEfficiency, c_index)
//						* pow(1. - mean_cJetEfficiency, numberOf_c_Jets - c_index)
//						* pow(mean_udsgJetEfficiency, udsg_index)
//						* pow(1. - mean_udsgJetEfficiency, numberOf_udsg_Jets - udsg_index);
//
//				probabilityData = pow(mean_bJetEfficiency * scaleFactor_b, b_index)
//						* pow(1. - mean_bJetEfficiency * scaleFactor_b, numberOf_b_Jets - b_index)
//						* pow(mean_cJetEfficiency * scaleFactor_c, c_index)
//						* pow(1. - mean_cJetEfficiency * scaleFactor_c, numberOf_c_Jets - c_index)
//						* pow(mean_udsgJetEfficiency * scaleFactor_udsg, udsg_index)
//						* pow(1. - mean_udsgJetEfficiency * scaleFactor_udsg, numberOf_udsg_Jets - udsg_index);
//
//				if (probabilityMC == 0)
//					event_weights.at(t) = 0;
//				else
//					event_weights.at(t) = probabilityData / probabilityMC;
//			}
//	return event_weights;
//}
//
//std::vector<double> BTagWeight::weights(double averageScaleFactor, unsigned int numberOfTags) const {
//	std::vector<double> event_weights;
//	for (unsigned int i = 0; i < numberOfTags + 1; ++i)
//		event_weights.push_back(0);
//	event_weights.at(0) = pow(1 - averageScaleFactor, numberOfTags);
//
//	if (numberOfTags > 0) {
//		for (unsigned int i = 1; i <= numberOfTags; ++i) {
//			double prod = 1;
//			for (unsigned int j = 1; j <= numberOfTags; ++j) {
//				if (j != i)
//					prod *= 1 - averageScaleFactor;
//			}
//			event_weights.at(1) += averageScaleFactor * prod;
//		}
//	}
//
//	if (numberOfTags > 1) {
//		for (unsigned int i = 1; i <= numberOfTags; ++i) {
//			double sum(0);
//			for (unsigned int j = 1; j <= numberOfTags; ++j) {
//				if (j == i)
//					continue;
//				double prod(1);
//				for (unsigned int k = 1; k <= numberOfTags; ++k) {
//					if (k != i && k != j)
//						prod *= 1 - averageScaleFactor;
//				}
//				sum += averageScaleFactor * prod;
//			}
//			event_weights.at(2) += averageScaleFactor * sum;
//		}
//		event_weights.at(2) = event_weights.at(2) / 2;
//	}
//	return event_weights;
//}

JetCollection BTagWeight::getBJets(const JetCollection& jets) const {
	JetCollection bjets;
	for (unsigned int index = 0; index < jets.size(); ++index) {
		if (abs(jets.at(index).partonFlavour()) == 5) //b-quark
			bjets.push_back(jets.at(index));
	}
	return bjets;
}

JetCollection BTagWeight::getCJets(const JetCollection& jets) const {
	JetCollection cjets;
	for (unsigned int index = 0; index < jets.size(); ++index) {
		if (abs(jets.at(index).partonFlavour()) == 4) //c-quark
			cjets.push_back(jets.at(index));
	}
	return cjets;
}

JetCollection BTagWeight::getUDSGJets(const JetCollection& jets) const {
	JetCollection udsgjets;
	for (unsigned int index = 0; index < jets.size(); ++index) {
		if (abs(jets.at(index).partonFlavour()) != 4 && abs(jets.at(index).partonFlavour()) != 5) //not a c- or b-quark
			udsgjets.push_back(jets.at(index));
	}
	return udsgjets;
}

double BTagWeight::getAverageBScaleFactor(const JetCollection& jets, std::string MCSampleTag, double uncertaintyFactor) const {
	std::vector<double> scaleFactors;

	for (unsigned int index = 0; index < jets.size(); ++index) {
		const Jet jet(jets.at(index));
		scaleFactors.push_back(getBScaleFactor(jet, MCSampleTag, uncertaintyFactor));
	}
	double sumOfScaleFactors = std::accumulate(scaleFactors.begin(), scaleFactors.end(), 0.0);
	if (scaleFactors.size() == 0) {
		return 1.;
	} else {
		return sumOfScaleFactors / scaleFactors.size();
	}
}

double BTagWeight::getBScaleFactor(const Jet& jet, std::string MCSampleTag, double uncertaintyFactor) const {
	double SFb(0);
	double sf_error(0);
	//these numbers are for CSVM only
	double pt = getSmearedJetPtScale(jet, 0)*jet.pt();
	double eta = jet.eta();

	if (MCSampleTag == "Summer12") { // 2012 btag scale factors
		// From https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-pt_WITHttbar_payload_EPS13.txt,
		// which is linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG#2012_Data_and_MC_EPS13_prescript
		const boost::array<double, 16> SFb_error = { { 0.0415707,
				0.0204209,
				0.0223227,
				0.0206655,
				0.0199325,
				0.0174121,
				0.0202332,
				0.0182446,
				0.0159777,
				0.0218531,
				0.0204688,
				0.0265191,
				0.0313175,
				0.0415417,
				0.0740446,
				0.0596716 } };

		//2012 pt bins low edges
		const boost::array<double, 16> ptbins = { { 20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 600 } };

		if (pt < 20) {
			SFb = (0.938887 + (0.00017124 * 20)) + (-2.76366e-07 * (20 * 20));
			//use twice the uncertainty
			sf_error = 2 * SFb_error[0];

		} else if (pt > 800) {
			SFb = (0.938887 + (0.00017124 * 800)) + (-2.76366e-07 * (800 * 800));
			//use twice the uncertainty
			sf_error = 2 * SFb_error[SFb_error.size() - 1];

		} else {
			SFb = (0.938887 + (0.00017124 * pt)) + (-2.76366e-07 * (pt * pt));
			unsigned int ptbin(0);
			for (unsigned int bin = 0; bin < ptbins.size() + 1; ++bin) {
				double upperCut = bin + 1 < ptbins.size() ? ptbins.at(bin + 1) : 800.;
				double lowerCut = ptbins.at(bin);

				if (pt > lowerCut && pt <= upperCut) {
					ptbin = bin;
					break;
				}
			}
			sf_error = SFb_error.at(ptbin);

			//use twice the uncertainty if outside the 0 to 2.4 eta range
			if (2.4 < eta && eta <= 2.6) {
				sf_error = 2 * SFb_error.at(ptbin);
			}
		}
	} else if (MCSampleTag == "Summer11Leg") { // 2011 btag scale factors
		// https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-mujet_payload.txt
		const boost::array<double, 14> SFb_error = { { 0.0295675,
				0.0295095,
				0.0210867,
				0.0219349,
				0.0227033,
				0.0204062,
				0.0185857,
				0.0256242,
				0.0383341,
				0.0409675,
				0.0420284,
				0.0541299,
				0.0578761,
				0.0655432 } };

		//2011 pt bins low edges
		const boost::array<double, 14> ptbins = { { 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500 } };

		if (pt < 30) {
			SFb = 0.6981 * ((1. + (0.414063 * pt)) / (1. + (0.300155 * 30)));
			//absolute uncertainty of +/-0.12
			sf_error = 0.12;

		} else if (pt > 670) {
			SFb = 0.6981 * ((1. + (0.414063 * 670)) / (1. + (0.300155 * 670)));
			//use twice the uncertainty
			sf_error = 2 * SFb_error[SFb_error.size() - 1];

		} else {
			SFb = 0.6981 * ((1. + (0.414063 * pt)) / (1. + (0.300155 * pt)));

			unsigned int ptbin(0);
			for (unsigned int bin = 0; bin < ptbins.size() + 1; ++bin) {
				double upperCut = bin + 1 < ptbins.size() ? ptbins.at(bin + 1) : 670.;
				double lowerCut = ptbins.at(bin);

				if (pt > lowerCut && pt <= upperCut) {
					ptbin = bin;
					break;
				}
			}
			sf_error = SFb_error.at(ptbin);
		}
	}
	SFb += sf_error * BJetSystematic_ * uncertaintyFactor;
	return SFb;
}

double BTagWeight::getAverageCScaleFactor(const JetCollection& jets, std::string MCSampleTag) const {
	// Same in both 8TeV and 7TeV
	return getAverageBScaleFactor(jets, MCSampleTag, 2.0); //SF_c = SF_b with twice the uncertainty
}

double BTagWeight::getCScaleFactor(const Jet& jet, std::string MCSampleTag) const {
	// Same in both 8TeV and 7TeV
	return getBScaleFactor(jet, MCSampleTag, 2.0);
}

double BTagWeight::getAverageUDSGScaleFactor(const JetCollection& jets, std::string MCSampleTag) const {
	std::vector<double> scaleFactors;

	for (unsigned int index = 0; index < jets.size(); ++index) {
		const Jet jet(jets.at(index));
		scaleFactors.push_back(getUDSGScaleFactor(jet, MCSampleTag));
	}
	double sumOfScaleFactors = std::accumulate(scaleFactors.begin(), scaleFactors.end(), 0.0);
	if (scaleFactors.size() == 0) {
		return 1.;
	} else {
		return sumOfScaleFactors / scaleFactors.size();
	}
}

double BTagWeight::getUDSGScaleFactor(const Jet& jet, std::string MCSampleTag) const {
	double pt = getSmearedJetPtScale(jet, 0)*jet.pt();
	double eta = jet.eta();
	double SF_udsg_mean(0), SF_udsg_min(0), SF_udsg_max(0);

	if (MCSampleTag == "Summer12") { // 2012
		if (pt < 20) {
			return 0;
		} else if (pt > 850 && eta >= 1.6 && eta <= 2.4) {
			SF_udsg_mean = getMeanUDSGScaleFactor(850., eta, MCSampleTag);
			SF_udsg_min = getMinUDSGScaleFactor(850, eta, MCSampleTag);
			SF_udsg_max = getMaxUDSGScaleFactor(850, eta, MCSampleTag);
			//use twice the uncertainty
			SF_udsg_min -= (SF_udsg_mean - SF_udsg_min);
			SF_udsg_max += (SF_udsg_max - SF_udsg_mean);
		} else if (pt > 1000) {
			SF_udsg_mean = getMeanUDSGScaleFactor(1000., eta, MCSampleTag);
			SF_udsg_min = getMinUDSGScaleFactor(1000, eta, MCSampleTag);
			SF_udsg_max = getMaxUDSGScaleFactor(1000, eta, MCSampleTag);
			//use twice the uncertainty
			SF_udsg_min -= (SF_udsg_mean - SF_udsg_min);
			SF_udsg_max += (SF_udsg_max - SF_udsg_mean);
		} else {
			SF_udsg_mean = getMeanUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_min = getMinUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_max = getMaxUDSGScaleFactor(pt, eta, MCSampleTag);
		}
	} else if (MCSampleTag == "Summer11Leg") { // 2011
		if (pt < 20) {
			return 0;
		} else if (pt > 670 && eta >= 0. && eta <= 2.4) {
			// Use integrated over all eta
			SF_udsg_mean = getMeanUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_min = getMinUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_max = getMaxUDSGScaleFactor(pt, eta, MCSampleTag);
			//use twice the uncertainty
			SF_udsg_min -= (SF_udsg_mean - SF_udsg_min);
			SF_udsg_max += (SF_udsg_max - SF_udsg_mean);
		} else {
			SF_udsg_mean = getMeanUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_min = getMinUDSGScaleFactor(pt, eta, MCSampleTag);
			SF_udsg_max = getMaxUDSGScaleFactor(pt, eta, MCSampleTag);
		}
	}

	if (LightJetSystematic_ == -1) {
		return SF_udsg_min;
	} else if (LightJetSystematic_ == 1) {
		return SF_udsg_max;
	}
	return SF_udsg_mean;
}

double BTagWeight::getMeanUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const {
	// From https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs_EPS2013.C
	// which is linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG#2012_Data_and_MC_EPS13_prescript

	if (MCSampleTag == "Summer12") { // 2012
		if (jetEta >=0 && jetEta < 0.8) {
			return ((1.07541+(0.00231827*jetPT))+(-4.74249e-06*(jetPT*jetPT)))+(2.70862e-09*(jetPT*(jetPT*jetPT)));
		} else if(jetEta >= 0.8 && jetEta < 1.6) {
			return ((1.05613+(0.00114031*jetPT))+(-2.56066e-06*(jetPT*jetPT)))+(1.67792e-09*(jetPT*(jetPT*jetPT)));
		} else if(jetEta >= 1.6 && jetEta <= 2.4){
			return ((1.05625+(0.000487231*jetPT))+(-2.22792e-06*(jetPT*jetPT)))+(1.70262e-09*(jetPT*(jetPT*jetPT)));
		}
	} else if (MCSampleTag == "Summer11Leg") { // 2011
		if (jetPT > 670 && jetEta >=0. && jetEta <= 2.4){ // Integrated over eta
			return ((1.04318+(0.000848162*jetPT))+(-2.5795e-06*(jetPT*jetPT)))+(1.64156e-09*(jetPT*(jetPT*jetPT)));
		} else if(jetEta >= 0 && jetEta < 0.8) {
			return ((1.06182+(0.000617034*jetPT))+(-1.5732e-06*(jetPT*jetPT)))+(3.02909e-10*(jetPT*(jetPT*jetPT)));
		} else if(jetEta >= 0.8 && jetEta < 1.6) {
			return ((1.111+(-9.64191e-06*jetPT))+(1.80811e-07*(jetPT*jetPT)))+(-5.44868e-10*(jetPT*(jetPT*jetPT)));
		} else if(jetEta >= 1.6 && jetEta <= 2.4) {
			return ((1.08498+(-0.000701422*jetPT))+(3.43612e-06*(jetPT*jetPT)))+(-4.11794e-09*(jetPT*(jetPT*jetPT)));
		}
	}
	return 0.;
}

double BTagWeight::getMinUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const {
	// From https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs_EPS2013.C
	// which is linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG#2012_Data_and_MC_EPS13_prescript

	if (MCSampleTag == "Summer12") { // 2012
			if (jetEta >=0 && jetEta < 0.8) {
				return ((0.964527+(0.00149055*jetPT))+(-2.78338e-06*(jetPT*jetPT)))+(1.51771e-09*(jetPT*(jetPT*jetPT)));
			} else if (jetEta >= 0.8 && jetEta < 1.6) {
				return ((0.946051+(0.000759584*jetPT))+(-1.52491e-06*(jetPT*jetPT)))+(9.65822e-10*(jetPT*(jetPT*jetPT)));
			} else if (jetEta >-1.6 && jetEta <= 2.4) {
			return ((0.956736 + (0.000280197 * jetPT)) + (-1.42739e-06 * (jetPT * jetPT))) + (1.0085e-09 * (jetPT * (jetPT * jetPT)));
		}
	}
	if (MCSampleTag == "Summer11Leg") { //2011
		if (jetPT > 670 && jetEta >= 0. && jetEta <= 2.4) { // Integrated over eta
			return ((0.962627 + (0.000448344 * jetPT)) + (-1.25579e-06 * (jetPT * jetPT))) + (4.82283e-10 * (jetPT * (jetPT * jetPT)));
		} else if (jetEta >= 0 && jetEta < 0.8) {
			return ((0.972455 + (7.51396e-06 * jetPT)) + (4.91857e-07 * (jetPT * jetPT))) + (-1.47661e-09 * (jetPT * (jetPT * jetPT)));
		} else if (jetEta >= 0.8 && jetEta < 1.6) {
			return ((1.02055 + (-0.000378856 * jetPT)) + (1.49029e-06 * (jetPT * jetPT))) + (-1.74966e-09 * (jetPT * (jetPT * jetPT)));
		} else if (jetEta >= 1.6 && jetEta < 2.4) {
			return ((0.983476 + (-0.000607242 * jetPT)) + (3.17997e-06 * (jetPT * jetPT))) + (-4.01242e-09 * (jetPT * (jetPT * jetPT)));
		}
	}
	return 0.;
}

double BTagWeight::getMaxUDSGScaleFactor(double jetPT, double jetEta, std::string MCSampleTag) const {
 	// From https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs_EPS2013.C
 	// which is linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG#2012_Data_and_MC_EPS13_prescript
	if (MCSampleTag == "Summer12") { // 2012
		if (jetEta >-0. && jetEta < 0.8) {
			return ((1.18638+(0.00314148*jetPT))+(-6.68993e-06*(jetPT*jetPT)))+(3.89288e-09*(jetPT*(jetPT*jetPT)));
		} else if (jetEta >= 0.8 && jetEta < 1.6) {
			return ((1.16624+(0.00151884*jetPT))+(-3.59041e-06*(jetPT*jetPT)))+(2.38681e-09*(jetPT*(jetPT*jetPT)));
		} else if (jetEta >= 1.6 && jetEta <= 2.4) {
			return ((1.15575+(0.000693344*jetPT))+(-3.02661e-06*(jetPT*jetPT)))+(2.39752e-09*(jetPT*(jetPT*jetPT)));
		}
	} else if (MCSampleTag == "Summer11Leg") { // 2011
		if (jetEta >670 && jetEta >=0. && jetEta <=2.4){
			// Integrated over eta
			return ((1.12368+(0.00124806*jetPT))+(-3.9032e-06*(jetPT*jetPT)))+(2.80083e-09*(jetPT*(jetPT*jetPT)));
		}else if (jetEta >= 0 && jetEta < 0.8) {
			return ((1.15116+(0.00122657*jetPT))+(-3.63826e-06*(jetPT*jetPT)))+(2.08242e-09*(jetPT*(jetPT*jetPT)));
		} else if (jetEta >= 0.8 && jetEta < 1.6) {
			return ((1.20146+(0.000359543*jetPT))+(-1.12866e-06*(jetPT*jetPT)))+(6.59918e-10*(jetPT*(jetPT*jetPT)));
		} else if (jetEta >= 1.6 && jetEta <= 2.4) {
			return ((1.18654+(-0.000795808*jetPT))+(3.69226e-06*(jetPT*jetPT)))+(-4.22347e-09*(jetPT*(jetPT*jetPT)));
		}
	}
	return 0.;
}

double BTagWeight::getAverageBEfficiency() const {
	double discriminator_cut = 0.679; //== CSVM
	return -1.73338329789 * pow(discriminator_cut, 4) + 1.26161794785 * pow(discriminator_cut, 3)
			+ 0.784721653518 * pow(discriminator_cut, 2) + -1.03328577451 * discriminator_cut + 1.04305075822;

}

double BTagWeight::getAverageCEfficiency() const {
	double discriminator_cut = 0.679; //== CSVM
	return -1.5734604211 * pow(discriminator_cut, 4) + 1.52798999269 * pow(discriminator_cut, 3)
			+ 0.866697059943 * pow(discriminator_cut, 2) + -1.66657942274 * discriminator_cut + 0.780639301724;

}

double BTagWeight::getAverageUDSGEfficiency(const JetCollection& jets) const {
	std::vector<double> efficiencies;

	for (unsigned int index = 0; index < jets.size(); ++index) {
		const Jet jet(jets.at(index));
		double efficiency(0);
		//these numbers are for CSVM only
		double pt = getSmearedJetPtScale(jet, 0)*jet.pt();
		if (pt < 20) {
			continue;
		} else if (pt > 800) {
			efficiency = getMeanUDSGEfficiency(800.);
		} else {
			efficiency = getMeanUDSGEfficiency(pt);
		}
		efficiencies.push_back(efficiency);
	}
	double sumOfEfficiencies = std::accumulate(efficiencies.begin(), efficiencies.end(), 0.0);
	if (efficiencies.size() == 0)
		return 1.;
	else
		return sumOfEfficiencies / efficiencies.size();
}

double BTagWeight::getMeanUDSGEfficiency(double jetPT) const {
	return 0.0113428 + 5.18983e-05 * jetPT - 2.59881e-08 * pow(jetPT, 2);
}

void BTagWeight::setNumberOfBtags(unsigned int min, unsigned int max) {
	minNumberOfTags_ = min;
	maxNumberOfTags_ = max;

}
