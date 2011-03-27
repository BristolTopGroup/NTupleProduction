#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Muons.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"

BristolNTuple_Muons::BristolNTuple_Muons(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag> ("InputTag")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix")),
    maxSize(iConfig.getParameter<unsigned int> ("MaxSize")),
    storePFIsolation(iConfig.getParameter<bool> ("storePFIsolation")),
    vtxInputTag(iConfig.getParameter<edm::InputTag> ("VertexInputTag")) {

    produces<std::vector<double> > (prefix + "Px" + suffix);
    produces<std::vector<double> > (prefix + "Py" + suffix);
    produces<std::vector<double> > (prefix + "Pz" + suffix);
    produces<std::vector<double> > (prefix + "TrkIso03" + suffix);
    produces<std::vector<double> > (prefix + "EcalIso03" + suffix);
    produces<std::vector<double> > (prefix + "HcalIso03" + suffix);
    produces<std::vector<int> > (prefix + "isGoodGlobalMuon" + suffix);
    if (storePFIsolation) {
        produces<std::vector<double> > (prefix + "PfChargedHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PfNeutralHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PFGammaIso" + suffix);
    }

    produces<std::vector<double> > (prefix + "Eta" + suffix);
    produces<std::vector<double> > (prefix + "Phi" + suffix);
    produces<std::vector<double> > (prefix + "Pt" + suffix);
    produces<std::vector<double> > (prefix + "P" + suffix);
    produces<std::vector<double> > (prefix + "Energy" + suffix);
    produces<std::vector<int> > (prefix + "Charge" + suffix);
    produces<std::vector<int> > (prefix + "TrkHits" + suffix);
    produces<std::vector<double> > (prefix + "TrkD0" + suffix);
    produces<std::vector<double> > (prefix + "TrkD0Error" + suffix);
    produces<std::vector<double> > (prefix + "TrkDz" + suffix);
    produces<std::vector<double> > (prefix + "TrkDzError" + suffix);
    produces<std::vector<double> > (prefix + "GlobalChi2" + suffix);
    produces<std::vector<double> > (prefix + "TrkIso" + suffix);
    produces<std::vector<double> > (prefix + "EcalIso" + suffix);
    produces<std::vector<double> > (prefix + "HcalIso" + suffix);
    produces<std::vector<double> > (prefix + "HOIso" + suffix);
    produces<std::vector<int> > (prefix + "VtxIndex" + suffix);
    produces<std::vector<double> > (prefix + "VtxDistXY" + suffix);
    produces<std::vector<double> > (prefix + "VtxDistZ" + suffix);

    produces<std::vector<double> > (prefix + "CocktailEta" + suffix);
    produces<std::vector<double> > (prefix + "CocktailPhi" + suffix);
    produces<std::vector<double> > (prefix + "CocktailPt" + suffix);
    produces<std::vector<double> > (prefix + "CocktailP" + suffix);
    produces<std::vector<int> > (prefix + "CocktailCharge" + suffix);
    produces<std::vector<int> > (prefix + "CocktailTrkHits" + suffix);
    produces<std::vector<double> > (prefix + "CocktailTrkD0" + suffix);
    produces<std::vector<double> > (prefix + "CocktailTrkD0Error" + suffix);
    produces<std::vector<double> > (prefix + "CocktailTrkDz" + suffix);
    produces<std::vector<double> > (prefix + "CocktailTrkDzError" + suffix);
    produces<std::vector<double> > (prefix + "CocktailGlobalChi2" + suffix);

}

void BristolNTuple_Muons::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso03(new std::vector<double>());
    std::auto_ptr < std::vector<int> > isGoodGlobalMuon(new std::vector<int>());
    std::auto_ptr < std::vector<double> > PfChargedHadronIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > PfNeutralHadronIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > PFGammaIso(new std::vector<double>());

    std::auto_ptr < std::vector<double> > eta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > phi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pt(new std::vector<double>());
    std::auto_ptr < std::vector<double> > p(new std::vector<double>());
    std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
    std::auto_ptr < std::vector<int> > charge(new std::vector<int>());
    std::auto_ptr < std::vector<int> > trkHits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > trkD0(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkD0Error(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkDz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkDzError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > globalChi2(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hoIso(new std::vector<double>());
    std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
    std::auto_ptr < std::vector<double> > vtxDistXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > vtxDistZ(new std::vector<double>());

    std::auto_ptr < std::vector<double> > ctEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctPhi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctPt(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctP(new std::vector<double>());
    std::auto_ptr < std::vector<int> > ctCharge(new std::vector<int>());
    std::auto_ptr < std::vector<int> > ctTrkHits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > ctTrkD0(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkD0Error(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkDz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkDzError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctGlobalChi2(new std::vector<double>());

    //-----------------------------------------------------------------
    edm::Handle < std::vector<pat::Muon> > muons;
    iEvent.getByLabel(inputTag, muons);

    edm::Handle < reco::VertexCollection > primaryVertices;
    iEvent.getByLabel(vtxInputTag, primaryVertices);

    if (muons.isValid()) {
        edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muons->size();

        for (std::vector<pat::Muon>::const_iterator it = muons->begin(); it != muons->end(); ++it) {
            // exit from loop when you reach the required number of muons
            if (px->size() >= maxSize)
                break;
            if (!it->isGlobalMuon())
                continue;
            const reco::TrackRef& cocktail_track = pmcTrack(*it);
            double trkd0 = it->track()->d0();
            double cttrkd0 = cocktail_track->d0();

            double minVtxDist3D = 9999.;
            int vtxIndex_ = -1;
            double vtxDistXY_ = -9999.;
            double vtxDistZ_ = -9999.;

            if (primaryVertices.isValid()) {
                edm::LogInfo("RootTupleMakerV2_MuonsInfo") << "Total # Primary Vertices: " << primaryVertices->size();

                for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it
                        != primaryVertices->end(); ++v_it) {

                    double distXY = it->track()->dxy(v_it->position());
                    double distZ = it->track()->dz(v_it->position());
                    double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

                    if (dist3D < minVtxDist3D) {
                        minVtxDist3D = dist3D;
                        vtxIndex_ = int(std::distance(primaryVertices->begin(), v_it));
                        vtxDistXY_ = distXY;
                        vtxDistZ_ = distZ;
                    }
                }
            } else {
                edm::LogError("RootTupleMakerV2_MuonsError") << "Error! Can't get the product " << vtxInputTag;
            }

            px->push_back(it->px());
            py->push_back(it->py());
            pz->push_back(it->pz());
            trkIso03->push_back(it->isolationR03().sumPt);
            ecalIso03->push_back(it->isolationR03().emEt);
            hcalIso03->push_back(it->isolationR03().hadEt);
            isGoodGlobalMuon->push_back((it->isGood("AllGlobalMuons")) ? 1 : 0);
            if (storePFIsolation) {
                pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
                pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
                pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);

                const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
                const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
                const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
                if (PfChargedHadronIsolation)
                    PfChargedHadronIso->push_back(PfChargedHadronIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
                            << "PfChargedHadronIsolation";
                if (PfNeutralHadronIsolation)
                    PfNeutralHadronIso->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
                            << "PfNeutralHadronIsolation";
                if (PFGammaIsolation)
                    PFGammaIso->push_back(PFGammaIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
                            << "PFGammaIsolation";

            }

            eta->push_back(it->eta());
            phi->push_back(it->phi());
            pt->push_back(it->pt());
            p->push_back(it->p());
            charge->push_back(it->charge());
            trkHits->push_back(it->track()->numberOfValidHits());
            trkD0->push_back(trkd0);
            trkD0Error->push_back(it->track()->d0Error());
            trkDz->push_back(it->track()->dz());
            trkDzError->push_back(it->track()->dzError());
            globalChi2->push_back(it->track()->normalizedChi2());

            ctEta ->push_back(cocktail_track->eta());
            ctPhi ->push_back(cocktail_track->phi());
            ctPt ->push_back(cocktail_track->pt());
            ctP ->push_back(cocktail_track->p());
            ctCharge ->push_back(cocktail_track->charge());
            ctTrkHits ->push_back(cocktail_track->numberOfValidHits());
            ctTrkD0 ->push_back(cttrkd0);
            ctTrkD0Error->push_back(cocktail_track->d0Error());
            ctTrkDz ->push_back(cocktail_track->dz());
            ctTrkDzError->push_back(cocktail_track -> dzError());
            ctGlobalChi2->push_back(cocktail_track ->normalizedChi2());

            energy->push_back(it->energy());
            trkIso->push_back(it->trackIso());
            ecalIso->push_back(it->ecalIso());
            hcalIso->push_back(it->hcalIso());
            hoIso->push_back(it->isolationR03().hoEt);

            vtxIndex->push_back(vtxIndex_);
            vtxDistXY->push_back(vtxDistXY_);
            vtxDistZ->push_back(vtxDistZ_);
        }
    } else {
        edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the product " << inputTag;
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put(trkIso03, prefix + "TrkIso03" + suffix);
    iEvent.put(ecalIso03, prefix + "EcalIso03" + suffix);
    iEvent.put(hcalIso03, prefix + "HcalIso03" + suffix);
    iEvent.put(isGoodGlobalMuon, prefix + "isGoodGlobalMuon" + suffix);
    if (storePFIsolation) {
        iEvent.put(PfChargedHadronIso, prefix + "PfChargedHadronIso" + suffix);
        iEvent.put(PfNeutralHadronIso, prefix + "PfNeutralHadronIso" + suffix);
        iEvent.put(PFGammaIso, prefix + "PFGammaIso" + suffix);
    }

    iEvent.put( eta, prefix + "Eta" + suffix );
      iEvent.put( phi, prefix + "Phi" + suffix );
      iEvent.put( pt, prefix + "Pt" + suffix );
      iEvent.put( p, prefix + "P" + suffix );
      iEvent.put( energy, prefix + "Energy" + suffix );
      iEvent.put( charge, prefix + "Charge" + suffix );
      iEvent.put( trkHits, prefix + "TrkHits" + suffix );
      iEvent.put( trkD0, prefix + "TrkD0" + suffix );
      iEvent.put( trkD0Error, prefix + "TrkD0Error" + suffix );
      iEvent.put( trkDz, prefix + "TrkDz" + suffix );
      iEvent.put( trkDzError, prefix + "TrkDzError" + suffix );
      iEvent.put( globalChi2, prefix + "GlobalChi2" + suffix );
      iEvent.put( trkIso, prefix + "TrkIso" + suffix );
      iEvent.put( ecalIso, prefix + "EcalIso" + suffix );
      iEvent.put( hcalIso, prefix + "HcalIso" + suffix );
      iEvent.put( hoIso, prefix + "HOIso" + suffix );
      iEvent.put( vtxIndex, prefix + "VtxIndex" + suffix );
      iEvent.put( vtxDistXY, prefix + "VtxDistXY" + suffix );
      iEvent.put( vtxDistZ, prefix + "VtxDistZ" + suffix );

      iEvent.put( ctEta       , prefix + "CocktailEta"        + suffix ) ;
      iEvent.put( ctPhi       , prefix + "CocktailPhi"        + suffix ) ;
      iEvent.put( ctPt        , prefix + "CocktailPt"         + suffix ) ;
      iEvent.put( ctP         , prefix + "CocktailP"          + suffix ) ;
      iEvent.put( ctCharge    , prefix + "CocktailCharge"     + suffix ) ;
      iEvent.put( ctTrkHits   , prefix + "CocktailTrkHits"    + suffix ) ;
      iEvent.put( ctTrkD0     , prefix + "CocktailTrkD0"      + suffix ) ;
      iEvent.put( ctTrkD0Error, prefix + "CocktailTrkD0Error" + suffix ) ;
      iEvent.put( ctTrkDz     , prefix + "CocktailTrkDz"      + suffix ) ;
      iEvent.put( ctTrkDzError, prefix + "CocktailTrkDzError" + suffix ) ;
      iEvent.put( ctGlobalChi2, prefix + "CocktailGlobalChi2" + suffix ) ;
}
