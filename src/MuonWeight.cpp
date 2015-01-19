#include "BristolAnalysis/NTupleTools/interface/MuonWeight.h"

#include <functional>
#include <numeric>
#include <boost/scoped_ptr.hpp>
#include <boost/array.hpp>

using namespace pat;


std::vector<double> MuonWeights(const pat::MuonCollection& muons, TH2F* muonIdIsoScaleFactorsHistogram, TH3F* muonTriggerScaleFactorsHistogram, int muonSystematicFactor, std::string MCSampleTag) {
	std::vector<double> muon_weights;

	for ( unsigned int muonIndex = 0; muonIndex < muons.size(); ++muonIndex ) {
		const pat::Muon& muon = muons.at(muonIndex);

		boost::scoped_ptr < MuonWeight > muonWeight ( new MuonWeight() );
		double muon_weight = muonWeight->weight ( muon, muonIdIsoScaleFactorsHistogram, muonTriggerScaleFactorsHistogram, muonSystematicFactor, MCSampleTag );

		muon_weights.push_back( muon_weight );
	}

	return muon_weights;
}

MuonWeight::MuonWeight() :
	Systematic_(0) {
}

double MuonWeight::weight( const Muon& muon, TH2F* muonIdIsoScaleFactorsHistogram, TH3F* muonTriggerScaleFactorsHistogram, int muonSystematicFactor, std::string MCSampleTag) const {

	double triggerSF = getTriggerScaleFactor( muon, muonTriggerScaleFactorsHistogram, MCSampleTag );
	double idSF = getIDScaleFactor( muon, muonIdIsoScaleFactorsHistogram, MCSampleTag );

	return triggerSF * idSF;
}

double MuonWeight::getTriggerScaleFactor( const pat::Muon& muon, TH3F* muonTriggerScaleFactorsHistogram, std::string MCSampleTag ) const {
	if (MCSampleTag == "Summer11Leg") {
		unsigned int triggerBinNumberMuon = muonTriggerScaleFactorsHistogram->FindBin( 1, muon.eta(), muon.pt() );
		unsigned int triggerBinNumberAntiMuon = muonTriggerScaleFactorsHistogram->FindBin( -1, muon.eta(), muon.pt() );

		if ( muon.pt() >= 2000 ) {
			triggerBinNumberMuon = muonTriggerScaleFactorsHistogram->FindBin( 1, muon.eta(), 1500 );
			triggerBinNumberAntiMuon = muonTriggerScaleFactorsHistogram->FindBin( -1, muon.eta(), 1500 );
		}

		float triggerScaleFactorMuon = muonTriggerScaleFactorsHistogram->GetBinContent( triggerBinNumberMuon );
		float triggerScaleFactorAntiMuon = muonTriggerScaleFactorsHistogram->GetBinContent( triggerBinNumberAntiMuon );

		return (triggerScaleFactorMuon + triggerScaleFactorAntiMuon) / 2;
	}
	else if ( MCSampleTag == "Summer12" ) {
		double id_correction = 1;
		double iso_correction = 1;
		double trigger_correction = 1;
		if (fabs(muon.eta()) < 0.9) { // 'ptabseta<0.9' in pickle file
				if ((10 <= muon.pt()) && (muon.pt() < 20)) {
						id_correction = 0.9702748917248193;
						iso_correction = 0.9403381500487888;
						trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
				}
				else if ((20 <= muon.pt()) && (muon.pt() < 25)) {
						id_correction = 0.9888647105027486;
						iso_correction = 0.9767384928595166;
						trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
				}
				else if ((25 <= muon.pt()) && (muon.pt() < 30)) {
						id_correction = 0.9923382289443887;
						iso_correction = 0.9961727553245637;
						trigger_correction = 0.9837252438433461;
				}
				else if ((30 <= muon.pt()) && (muon.pt() < 35)) {
						id_correction = 0.9932832435710769;
						iso_correction = 0.9932276697519965;
						trigger_correction = 0.9840634431547701;
				}
				else if ((35 <= muon.pt()) && (muon.pt() < 40)) {
						id_correction = 0.9936619045236875;
						iso_correction = 0.993713125125077;
						trigger_correction = 0.9839165818168554;
				}
				else if ((40 <= muon.pt()) && (muon.pt() < 50)) {
						id_correction = 0.9923918872503162;
						iso_correction = 0.9940841647892507;
						trigger_correction = 0.9834525270057036;
				}
				else if ((50 <= muon.pt()) && (muon.pt() < 60)) {
						id_correction = 0.9911899786643166;
						iso_correction = 0.9964353940407351;
						trigger_correction = 0.9842917703915748;
				}
				else if ((60 <= muon.pt()) && (muon.pt() < 90)) {
						id_correction = 0.9894167956611032;
						iso_correction = 0.9986584316076454;
						trigger_correction = 0.9846720184248945;
				}
				else if ((90 <= muon.pt()) && (muon.pt() < 140)) {
						id_correction = 1.0037489877154855;
						iso_correction = 1.0003297152126076;
						trigger_correction = 0.9809171165806959;
				}
				else if ((140 <= muon.pt()) && (muon.pt() < 300)) {
						id_correction = 1.0185025540365602;
						iso_correction = 0.998812853360961;
						trigger_correction = 0.9804174981053351; // given for pt '140_500' in pickle file
				}
		} else if ((fabs(muon.eta()) >= 0.9 && fabs(muon.eta()) < 1.2)) { // 'ptabseta0.9-1.2' in pickle file
			if ((10 <= muon.pt()) && (muon.pt() < 20)) {
					id_correction = 1.0017313093647269;
					iso_correction = 0.9484342057793206;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muon.pt()) && (muon.pt() < 25)) {
					id_correction = 0.9939466451892177;
					iso_correction = 0.9863669311896185;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muon.pt()) && (muon.pt() < 30)) {
					id_correction = 0.9947219657132994;
					iso_correction = 1.0003560413214891;
					trigger_correction = 0.9683812755993191;
			}
			else if ((30 <= muon.pt()) && (muon.pt() < 35)) {
					id_correction = 0.9933913481874554;
					iso_correction = 1.0000867333890535;
					trigger_correction = 0.965380548896101;
			}
			else if ((35 <= muon.pt()) && (muon.pt() < 40)) {
					id_correction = 0.9922848270630622;
					iso_correction = 0.9990915568314974;
					trigger_correction = 0.9669651415167049;
			}
			else if ((40 <= muon.pt()) && (muon.pt() < 50)) {
					id_correction = 0.9918700391817427;
					iso_correction = 0.9988684367869946;
					trigger_correction = 0.966679581608325;
			}
			else if ((50 <= muon.pt()) && (muon.pt() < 60)) {
					id_correction = 0.995010062219747;
					iso_correction = 0.9978903999478148;
					trigger_correction = 0.9627395755250187;
			}
			else if ((60 <= muon.pt()) && (muon.pt() < 90)) {
					id_correction = 0.99040605451701;
					iso_correction = 0.9992149992903525;
					trigger_correction = 0.9595241683475331;
			}
			else if ((90 <= muon.pt()) && (muon.pt() < 140)) {
					id_correction = 1.0090275981046186;
					iso_correction = 1.0014212099113895;
					trigger_correction = 0.9644418246112644;
			}
			else if ((140 <= muon.pt()) && (muon.pt() < 300)) {
					id_correction = 1.010956056270124;
					iso_correction = 1.0018540386614887;
					trigger_correction = 0.9712789619617556; // given for pt '140_500' in pickle file
			}
		} else if ((fabs(muon.eta()) >= 1.2 && fabs(muon.eta()) < 2.1)) { // 'ptabseta1.2-2.1' in pickle file
			if ((10 <= muon.pt()) && (muon.pt() < 20)) {
					id_correction = 1.0180184284620057;
					iso_correction = 0.9724367240900078;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muon.pt()) && (muon.pt() < 25)) {
					id_correction = 1.0003513994342943;
					iso_correction = 0.9900544131155273;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muon.pt()) && (muon.pt() < 30)) {
					id_correction = 0.9984860359215375;
					iso_correction = 1.0028199004178158;
					trigger_correction = 1.0051991254438037;
			}
			else if ((30 <= muon.pt()) && (muon.pt() < 35)) {
					id_correction = 0.9965584500063546;
					iso_correction = 1.0040456735929117;
					trigger_correction = 1.0013781590159485;
			}
			else if ((35 <= muon.pt()) && (muon.pt() < 40)) {
					id_correction = 0.996026448928709;
					iso_correction = 1.0021465355614672;
					trigger_correction = 0.99616640424792;
			}
			else if ((40 <= muon.pt()) && (muon.pt() < 50)) {
					id_correction = 0.9960618126306268;
					iso_correction = 1.0009158373782485;
					trigger_correction = 0.9942541014104305;
			}
			else if ((50 <= muon.pt()) && (muon.pt() < 60)) {
					id_correction = 0.9951827274866013;
					iso_correction = 1.0004039805545037;
					trigger_correction = 0.990544673012178;
			}
			else if ((60 <= muon.pt()) && (muon.pt() < 90)) {
					id_correction = 0.9924861810666658;
					iso_correction = 1.00050232016842;
					trigger_correction = 0.9882937419288585;
			}
			else if ((90 <= muon.pt()) && (muon.pt() < 140)) {
					id_correction = 1.023129380083607;
					iso_correction = 0.9991578234416382;
					trigger_correction = 0.9818759899390823;
			}
			else if ((140 <= muon.pt()) && (muon.pt() < 300)) {
					id_correction = 0.9747541719440429;
					iso_correction = 0.9964395746067783;
					trigger_correction = 0.9941686682904833; // given for pt '140_500' in pickle file
			}
		} else if (fabs(muon.eta()) >= 2.1 && fabs(muon.eta()) <= 2.4) { // 'ptabseta2.1-2.4' in pickle file. Note: Trigger scale factors only provided up to absolute eta of 2.1 in the link above, so I have used the same as for the 1.2 to 2.1 eta range.
			if ((10 <= muon.pt()) && (muon.pt() < 20)) {
					id_correction = 1.0050443332472756;
					iso_correction = 1.1167270384985806;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muon.pt()) && (muon.pt() < 25)) {
					id_correction = 0.9980890826544107;
					iso_correction = 1.1155400869984835;
					trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muon.pt()) && (muon.pt() < 30)) {
					id_correction = 0.9961828904505218;
					iso_correction = 1.096718301830121;
					trigger_correction = 1.0051991254438037;
			}
			else if ((30 <= muon.pt()) && (muon.pt() < 35)) {
					id_correction = 1.000551051988681;
					iso_correction = 1.074812169170078;
					trigger_correction = 1.0013781590159485;
			}
			else if ((35 <= muon.pt()) && (muon.pt() < 40)) {
					id_correction = 0.9925634188516349;
					iso_correction = 1.0605853576108657;
					trigger_correction = 0.99616640424792;
			}
			else if ((40 <= muon.pt()) && (muon.pt() < 50)) {
					id_correction = 0.9951441282077462;
					iso_correction = 1.0377065931130076;
					trigger_correction = 0.9942541014104305;
			}
			else if ((50 <= muon.pt()) && (muon.pt() < 60)) {
					id_correction = 0.993590319966609;
					iso_correction = 1.0252924559186363;
					trigger_correction = 0.990544673012178;
			}
			else if ((60 <= muon.pt()) && (muon.pt() < 90)) {
					id_correction = 0.9894841861002339;
					iso_correction = 1.0149496896687298;
					trigger_correction = 0.9882937419288585;
			}
			else if ((90 <= muon.pt()) && (muon.pt() < 140)) {
					id_correction = 1.0601733432927236;
					iso_correction = 1.0081292468302308;
					trigger_correction = 0.9818759899390823;
			}
			else if ((140 <= muon.pt()) && (muon.pt() < 300)) {
					id_correction = 0.890546814737379;
					iso_correction = 1.0106204522044593;
					trigger_correction = 0.9941686682904833; // given for pt '140_500' in pickle file
			}
		}
		return id_correction * iso_correction * trigger_correction;
	}
	else {
		return 1.;
	}
}

double MuonWeight::getIDScaleFactor( const pat::Muon& muon, TH2F* muonIdIsoScaleFactorsHistogram, std::string MCSampleTag ) const {
	if ( MCSampleTag == "Summer11Leg"){
		unsigned int isoBinNumberMuon = muonIdIsoScaleFactorsHistogram->FindBin( muon.eta(), muon.pt() );

		if ( muon.pt() >= 2000 ) {
			isoBinNumberMuon = muonIdIsoScaleFactorsHistogram->FindBin( muon.eta(), 1500 );
		}

		return muonIdIsoScaleFactorsHistogram->GetBinContent(isoBinNumberMuon);
	}
		else return 1;
}
