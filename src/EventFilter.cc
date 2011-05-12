#include "BristolAnalysis/NTupleTools/interface/EventFilter.h"
// system include files
#include <memory>

// user include files


#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

using namespace edm;
using namespace std;

EventFilter::EventFilter(const edm::ParameterSet& iConfig) :
    jetInput_(iConfig.getParameter<edm::InputTag> ("jetInput")),
    electronInput_(iConfig.getParameter<edm::InputTag> ("electronInput")),
    vertexInput_(iConfig.getParameter<edm::InputTag>("VertexInput")),
    hcalNoiseInput_(iConfig.getParameter<edm::InputTag>("HcalNoiseInput")),
    trkInput_(iConfig.getParameter<edm::InputTag>("TracksInput")),
    minNJets_(iConfig.getParameter<int> ("minNJets")),
    maxNJets_(iConfig.getParameter<int> ("maxNJets")),
    minNElectrons_(iConfig.getParameter<int> ("minNElectrons")),
    maxNElectrons_(iConfig.getParameter<int> ("maxNElectrons")),
    minJetPt(iConfig.getParameter<double> ("minJetPt")),
    maxAbsJetEta(iConfig.getParameter<double> ("maxAbsJetEta")),
    minElectronPt_(iConfig.getParameter<double> ("minElectronPt")),
    maxAbsElectronEta_(iConfig.getParameter<double> ("maxAbsElectronEta")),
    vtxMinNDOF(iConfig.getParameter<unsigned int>("VertexMinimumNDOF")),
    vtxMaxAbsZ(iConfig.getParameter<double>("VertexMaxAbsZ")),
    vtxMaxAbsRho(iConfig.getParameter<double>("VertexMaxAbsRho")),
    numTracks(iConfig.getParameter<unsigned int>("NumTracks")),
    hpTrackThreshold(iConfig.getParameter<double>("HPTrackThreshold")),

    debug_(iConfig.getUntrackedParameter<bool> ("debug")),
    totalCount(0),
    passHBHENoiseFilter(0),
    passScrapingVeto(0),
    passGoodPrimaryVertex(0),
    passElectronCuts(0),
    passJetCuts(0),
    hCount(){

    edm::Service<TFileService> histServ;

    hCount = histServ->make<TH1I> ("EventCounter", "Event Counter", 6, -0.5, 5.5);
    hCount->GetXaxis()->SetBinLabel(1, "all events");
    hCount->GetXaxis()->SetBinLabel(2, "HBHENoiseFilter");
    hCount->GetXaxis()->SetBinLabel(3, "ScrapingVeto");
    hCount->GetXaxis()->SetBinLabel(4, "GoodPrimaryVertex");
    hCount->GetXaxis()->SetBinLabel(5, "ElectronCuts");
    hCount->GetXaxis()->SetBinLabel(6, "JetCuts");
}

EventFilter::~EventFilter() {

}

bool EventFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ++totalCount;

    edm::Handle<bool> hbheFilterResult;
    iEvent.getByLabel(hcalNoiseInput_, hbheFilterResult);

    if (hbheFilterResult.isValid()) {
        edm::LogInfo("EventFilter") << "Successfully obtained " << hcalNoiseInput_;

    } else {
        edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << hcalNoiseInput_;
    }

    if(*hbheFilterResult == false)
        return false;
    ++passHBHENoiseFilter;

    // Scraping Events Part
    edm::Handle < reco::TrackCollection > tracks;
    iEvent.getByLabel(trkInput_, tracks);
    double fraction = 1.;

    if (tracks.isValid()) {
        edm::LogInfo("EventFilter") << "Total # Tracks: " << tracks->size();

        int numhighpurity = 0;

        reco::TrackBase::TrackQuality trackQuality = reco::TrackBase::qualityByName("highPurity");

        if (tracks->size() > numTracks) {
            for (reco::TrackCollection::const_iterator it = tracks->begin(); it != tracks->end(); ++it) {
                if (it->quality(trackQuality))
                    numhighpurity++;
            }
            fraction = (double) numhighpurity / (double) tracks->size();

        }
    } else {
        edm::LogError("EventFilterError") << "Error! Can't get the product " << trkInput_;
    }
    if (fraction < hpTrackThreshold)
        return false;


    ++passScrapingVeto;

    // Good Primary Vertex Part
    edm::Handle < reco::VertexCollection > primaryVertices;
    iEvent.getByLabel(vertexInput_, primaryVertices);
    int numGoodVertices(0);

    if (primaryVertices.isValid()) {
        edm::LogInfo("EventFilter") << "Total # Primary Vertices: " << primaryVertices->size();


        for (reco::VertexCollection::const_iterator it = primaryVertices->begin(); it != primaryVertices->end(); ++it) {
            if (!(it->isFake()) && it->ndof() >= vtxMinNDOF && fabs(it->z()) <= vtxMaxAbsZ && fabs(it->position().rho())
                    <= vtxMaxAbsRho)
                ++numGoodVertices;
        }
    } else {
        edm::LogError("EventFilterError") << "Error! Can't get the product " << vertexInput_;
    }
    if(numGoodVertices < 1)
        return false;

    ++passGoodPrimaryVertex;

    edm::Handle < edm::View<reco::Candidate> > jets;
    iEvent.getByLabel(jetInput_, jets);

    edm::Handle < edm::View<reco::Candidate> > electrons;
    iEvent.getByLabel(electronInput_, electrons);

    int nelectrons = 0;

    for (edm::View<reco::Candidate>::const_iterator it = electrons->begin(); it != electrons->end(); ++it) {
        if (debug_)
            cout << "Electron:" << endl;
        if (debug_)
            cout << "pT: " << it->pt() << " eta: " << it->eta() << " phi: " << it->phi() << endl;

        if (it->pt() > minElectronPt_ && fabs(it->eta()) < maxAbsElectronEta_) {
            ++nelectrons;
        }
    }

    if (debug_)
        cout << "# Electrons = " << nelectrons << endl;

    if (minNElectrons_ > -1 && nelectrons < minNElectrons_)
        return false;
    if (maxNElectrons_ > -1 && nelectrons > maxNElectrons_)
        return false;

    ++passElectronCuts;

    int njets = 0;

    for (edm::View<reco::Candidate>::const_iterator it = jets->begin(); it != jets->end(); ++it) {
        if (debug_)
            cout << "Jet:" << endl;
        if (debug_)
            cout << "pT: " << it->pt() << " eta: " << it->eta() << " phi: " << it->phi() << endl;
        if (it->pt() > minJetPt && fabs(it->eta()) < maxAbsJetEta) {
            ++njets;
        }
    }

    if (debug_)
        cout << "# Jets = " << njets << endl;
    // If not enough jets found (or too many found), return false
    if (minNJets_ > -1 && njets < minNJets_)
        return false;
    if (maxNJets_ > -1 && njets > maxNJets_)
        return false;

    ++passJetCuts;
    if (debug_)
        cout << "PASSED!" << endl;
    return true;
}

// ------------ method called once each job just before starting event loop  ------------
void EventFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void EventFilter::endJob() {
    hCount->SetBinContent(1, totalCount);
    hCount->SetBinContent(2, passHBHENoiseFilter);
    hCount->SetBinContent(3, passScrapingVeto);
    hCount->SetBinContent(4, passGoodPrimaryVertex);
    hCount->SetBinContent(5, passElectronCuts);
    hCount->SetBinContent(6, passJetCuts);

    cout << "Total events = " << totalCount << endl;
    cout << "passed  HBHENoiseFilter= " << passHBHENoiseFilter << endl;
    cout << "passed  ScrapingVeto= " << passScrapingVeto << endl;
    cout << "passed  GoodPrimaryVertex= " << passGoodPrimaryVertex << endl;
    cout << "passed  ElectronCuts= " << passElectronCuts << endl;
    cout << "passed  JetCuts= " << passJetCuts << endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE( EventFilter);
