#ifndef BristolTopSemiLeptonicEventFilter
#define BristolNTuplebeamSpot

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include <boost/array.hpp>
#include <string>
//#include "TH1.h"

namespace Selection {
enum value{
	EventCleaning,
	Trigger,
	ExactlyOneIsolatedLepton,
	LooseMuonVeto,
	LooseElectronVeto,
	ConvRejectionInnerHits,
	ConvRejectionPartnerTrack,
	OneJet,
	TwoJets,
	ThreeJets,
	FourJets,
	NUMBER_OF_SELECTION_STEPS
};

const std::string StringSteps[NUMBER_OF_SELECTION_STEPS] = {
        "Event Cleaning",
        "High Level Trigger",
        "exactly one isolated letpon",
        "loose muon veto",
        "loose electron veto",
        "Conversion veto (missing hits)",
        "Conversion finder (partner track)",
        ">= 1 jets",
        ">= 2 jets",
        ">= 3 jets",
        ">= 4 jets",
};
}

class TopSemiLeptonicEventFilter: public edm::EDFilter {
public:
    explicit TopSemiLeptonicEventFilter(const edm::ParameterSet&);
    virtual ~TopSemiLeptonicEventFilter();

private:
    virtual void beginJob();
    virtual bool filter(edm::Event&, const edm::EventSetup&);
    virtual void endJob();

    bool passesEventCleaning(edm::Event& iEvent) const;
    bool passesElectronTrigger() const;
    bool passesMuonTrigger() const;
//    bool passesLooseElectronVeto(const pat::Electron electron, const pat::ElectronCollection looseElectrons) const;

    pat::ElectronCollection cleanElectronsAgainstJets(const pat::ElectronCollection, const pat::JetCollection goodJets) const;
    pat::JetCollection cleanJetsAgainstElectrons(const pat::JetCollection goodJets, const pat::ElectronCollection) const;
    pat::ElectronCollection getGoodIsolatedElectrons(const pat::ElectronCollection electrons) const;
    pat::ElectronCollection getLooseElectrons(const pat::ElectronCollection electrons) const;
    pat::MuonCollection getLooseMuons(const pat::MuonCollection muons) const;
    pat::JetCollection getGoodJets(const pat::JetCollection jets) const;
    pat::ElectronCollection removeGoodIsolatedElectronsFromLooseElectrons(const pat::ElectronCollection goodElectrons,
			const pat::ElectronCollection looseElectrons) const;


    edm::InputTag jetInput_, electronInput_, muonInput_, vertexInput_, hcalNoiseInput_, trkInput_;

//    int minNJets_, maxNJets_, minNElectrons_, maxNElectrons_, minNMuons_, maxNMuons_;

    double minJetPt_, maxAbsJetEta_, minElectronPt_, maxAbsElectronEta_, minMuonPt_, maxAbsMuonEta_;

    double tightElectronIso_, looseElectronIso_, tightMuonIso_, looseMuonIso_;

    bool electronPlusJetsSelection_, muonPlusJetsSelection_, useTrigger_;

    const unsigned int vtxMinNDOF_;
    const double vtxMaxAbsZ_, vtxMaxAbsRho_;

    const unsigned int numTracks_;
    const double hpTrackThreshold_;

    bool debug_;
    boost::array<unsigned int, Selection::NUMBER_OF_SELECTION_STEPS> passes_;
    int totalCount;

//    TH1I* hCount;
};

#endif
