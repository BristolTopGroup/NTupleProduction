#include "BristolAnalysis/NTupleTools/interface/ElectronWeight.h"

#include <functional>
#include <numeric>
#include <boost/scoped_ptr.hpp>
#include <boost/array.hpp>

using namespace pat;


std::vector<double> ElectronWeights(const pat::ElectronCollection& electrons, const pat::Jet& jet, TH2F* electronIdIsoScaleFactorsHistogram, TEfficiency* electronTriggerEfficiencyHistogram, TH1F* hadronLegTriggerHistogram, int electronSystematicFactor, std::string MCSampleTag) {
	std::vector<double> electron_weights;

	for ( unsigned int electronIndex = 0; electronIndex < electrons.size(); ++electronIndex ) {
		const pat::Electron& electron = electrons.at(electronIndex);

		boost::scoped_ptr < ElectronWeight > electronWeight ( new ElectronWeight() );
		double electron_weight = electronWeight->weight ( electron, jet, electronIdIsoScaleFactorsHistogram, electronTriggerEfficiencyHistogram, hadronLegTriggerHistogram, electronSystematicFactor, MCSampleTag );

		electron_weights.push_back( electron_weight );
	}

	return electron_weights;
}

ElectronWeight::ElectronWeight() :
	Systematic_(0) {
}

double ElectronWeight::weight( const Electron& electron, const pat::Jet& jet, TH2F* electronIdIsoScaleFactorsHistogram, TEfficiency* electronTriggerEfficiencyHistogram, TH1F* hadronLegTriggerHistogram, int electronSystematicFactor, std::string MCSampleTag) const {

	double triggerSF = getTriggerScaleFactor( electron, electronTriggerEfficiencyHistogram, MCSampleTag );
	double idSF = getIDScaleFactor( electron, electronIdIsoScaleFactorsHistogram, MCSampleTag );
	double hadronLegEFficiency = getHadronLegTriggerEfficiency( jet, hadronLegTriggerHistogram, MCSampleTag );

	return triggerSF * idSF * hadronLegEFficiency;
}

double ElectronWeight::getTriggerScaleFactor( const pat::Electron& electron, TEfficiency* electronTriggerEfficiencyHistogram, std::string MCSampleTag ) const {
	if (MCSampleTag == "Summer11Leg") {
		unsigned int triggerBinNumberElectron = 1.;

		if ( electron.pt() >= 100 ) {
			triggerBinNumberElectron = electronTriggerEfficiencyHistogram->FindFixBin( 90, electron.eta() );
		}
		else{
			triggerBinNumberElectron = electronTriggerEfficiencyHistogram->FindFixBin( electron.pt(), electron.eta() );
		}

		return electronTriggerEfficiencyHistogram->GetEfficiency( triggerBinNumberElectron );
	}
	else if ( MCSampleTag == "Summer12" ) {
		double correction = 1;

		if(fabs(electron.eta())<0.8) {
			if(20<=electron.pt() && electron.pt()<30) {  //Note: Trigger scale factors only provided down to electron pt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.949*0.987;
			}
			else if(30<=electron.pt() && electron.pt()<40) {
				correction = 0.939*0.987;
			}
			else if(40<=electron.pt() && electron.pt()<50) {
				correction = 0.950*0.997;
			}
			else if(50<=electron.pt() && electron.pt()<=200) {
				correction = 0.957*0.998;
			}
		}
		else if(fabs(electron.eta())>=0.8 && fabs(electron.eta())<1.478) {
			if(20<=electron.pt() && electron.pt()<30) { //Note: Trigger scale factors only provided down to electron pt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.900*0.964;
			}
			if(30<=electron.pt() && electron.pt()<40) {
				correction = 0.920*0.964;
			}
			if(40<=electron.pt() && electron.pt()<50) {
				correction = 0.949*0.980;
			}
			if(50<=electron.pt() && electron.pt()<=200) {
				correction = 0.959*0.988;
			}
		}
		else if(fabs(electron.eta())>=1.478 && fabs(electron.eta())<2.5) {
			if(20<=electron.pt() && electron.pt()<30) { //Note: Trigger scale factors only provided down to electron pt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.857*1.004;
			}
			if(30<=electron.pt() && electron.pt()<40) {
				correction = 0.907*1.004;
			}
			if(40<=electron.pt() && electron.pt()<50) {
				correction = 0.937*1.033;
			}
			if(50<=electron.pt() && electron.pt()<=200) {
				correction = 0.954*0.976;
			}
		}
		return correction;
	}
	else {
		return 1.;
	}
}

double ElectronWeight::getIDScaleFactor( const pat::Electron& electron, TH2F* electronIdIsoScaleFactorsHistogram, std::string MCSampleTag ) const {
	if ( MCSampleTag == "Summer11Leg"){

		unsigned int isoBinNumberElectron = 1.;

		if ( electron.pt() >= 100 ) {
			isoBinNumberElectron = electronIdIsoScaleFactorsHistogram->FindBin( 90, electron.eta() );
		}
		else{
			isoBinNumberElectron = electronIdIsoScaleFactorsHistogram->FindBin( electron.pt(), electron.eta() );
		}

		return electronIdIsoScaleFactorsHistogram->GetBinContent( isoBinNumberElectron );

	}
	else return 1;
}

double ElectronWeight::getHadronLegTriggerEfficiency( const pat::Jet& jet, TH1F* hadronLegTriggerHistogram, std::string MCSampleTag ) const {
	if ( MCSampleTag == "Summer11Leg"){
		unsigned int binNumber = 1.;

		if ( jet.pt() > 100 ) {
			binNumber = hadronLegTriggerHistogram->FindBin( 90 );
		}
		else{
			binNumber = hadronLegTriggerHistogram->FindBin( jet.pt() );
		}
		return hadronLegTriggerHistogram->GetBinContent( binNumber );
	}
	else return 1.;
}

