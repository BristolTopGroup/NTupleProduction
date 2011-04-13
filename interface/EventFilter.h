#ifndef BristolEventFilter
#define BristolNTuplebeamSpot

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1.h"

class EventFilter: public edm::EDFilter {
public:
    explicit EventFilter(const edm::ParameterSet&);
    virtual ~EventFilter();

private:
    virtual void beginJob();
    virtual bool filter(edm::Event&, const edm::EventSetup&);
    virtual void endJob();

    edm::InputTag jetInput_, electronInput_, vertexInput_, hcalNoiseInput_, trkInput_;

    int minNJets_, maxNJets_, minNElectrons_, maxNElectrons_;

    double minJetPt, maxAbsJetEta, minElectronPt_, maxAbsElectronEta_;

    const unsigned int vtxMinNDOF;
    const double vtxMaxAbsZ, vtxMaxAbsRho;

    const unsigned int numTracks;
    const double hpTrackThreshold;

    bool debug_;

    int totalCount, passHBHENoiseFilter, passScrapingVeto, passGoodPrimaryVertex;
    int passElectronCuts, passJetCuts;

    TH1I* hCount;
};

#endif
