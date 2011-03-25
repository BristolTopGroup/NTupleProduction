#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Tracks.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/TrackReco/interface/Track.h"

BristolNTuple_Tracks::BristolNTuple_Tracks(const edm::ParameterSet& iConfig) :
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix"))
{
//    produces<std::vector<double> > (prefix + "NDOF" + suffix);
    produces<std::vector<int> > (prefix + "Charge" + suffix);
    produces<std::vector<double> > (prefix + "Pt" + suffix);
//    produces<std::vector<double> > (prefix + "PtError" + suffix);
//    produces<std::vector<double> > (prefix + "Px" + suffix);
//    produces<std::vector<double> > (prefix + "Py" + suffix);
//    produces<std::vector<double> > (prefix + "Pz" + suffix);
    produces<std::vector<double> > (prefix + "Eta" + suffix);
//    produces<std::vector<double> > (prefix + "EtaError" + suffix);
    produces<std::vector<double> > (prefix + "Phi" + suffix);
//    produces<std::vector<double> > (prefix + "PhiError" + suffix);
    produces<std::vector<double> > (prefix + "Theta" + suffix);
    produces<std::vector<double> > (prefix + "D0" + suffix);
//    produces<std::vector<double> > (prefix + "D0Error" + suffix);

//    produces<std::vector<double> > (prefix + "Dz" + suffix);
//    produces<std::vector<double> > (prefix + "DzError" + suffix);
    produces<std::vector<double> > (prefix + "Vx" + suffix);
    produces<std::vector<double> > (prefix + "Vy" + suffix);
    produces<std::vector<double> > (prefix + "Vz" + suffix);

//    produces<std::vector<double> > (prefix + "InnerPosition.x" + suffix);
//    produces<std::vector<double> > (prefix + "InnerPosition.y" + suffix);
//    produces<std::vector<double> > (prefix + "InnerPosition.z" + suffix);
//    produces<std::vector<double> > (prefix + "OuterPosition.x" + suffix);
//    produces<std::vector<double> > (prefix + "OuterPosition.y" + suffix);
//    produces<std::vector<double> > (prefix + "OuterPosition.z" + suffix);
//
//    produces<std::vector<int> > (prefix + "recHitsSize" + suffix);
//    produces<std::vector<int> > (prefix + "numberOfValidHits" + suffix);
//    produces<std::vector<int> > (prefix + "numberOfLostHits" + suffix);
    produces<std::vector<int> > (prefix + "innerLayerMissingHits" + suffix);
//    produces<std::vector<int> > (prefix + "innerLayerMissingHitsPixels" + suffix);
//    produces<std::vector<int> > (prefix + "numPixelHits" + suffix);
//    produces<std::vector<int> > (prefix + "numStripHits" + suffix);

    produces<std::vector<bool> > (prefix + "isHighPurity" + suffix);
//    produces<std::vector<bool> > (prefix + "hasValidHitInFirstPixelBarrel" + suffix);
}

void BristolNTuple_Tracks::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
//    std::auto_ptr < std::vector<double> > NDOF(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Pt(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > PtError(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > Px(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > Py(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > Pz(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Eta(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > EtaError(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Phi(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > PhiError(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Theta(new std::vector<double>());
    std::auto_ptr<std::vector<double> > D0(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > D0Error(new std::vector<double>());

//    std::auto_ptr<std::vector<double> > Dz(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > DzError(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Vx(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Vy(new std::vector<double>());
    std::auto_ptr<std::vector<double> > Vz(new std::vector<double>());

//    std::auto_ptr<std::vector<double> > InnerPositionX(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > InnerPositionY(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > InnerPositionZ(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > OuterPositionX(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > OuterPositionY(new std::vector<double>());
//    std::auto_ptr<std::vector<double> > OuterPositionZ(new std::vector<double>());

    std::auto_ptr < std::vector<int> > Charge(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > recHitsSize(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > numberOfValidHits(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > numberOfLostHits(new std::vector<int>());
    std::auto_ptr<std::vector<int> > innerLayerMissingHits(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > innerLayerMissingHitsPixels(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > numPixelHits(new std::vector<int>());
//    std::auto_ptr<std::vector<int> > numStripHits(new std::vector<int>());

    std::auto_ptr<std::vector<bool> > isHighPurity(new std::vector<bool>());
//    std::auto_ptr<std::vector<bool> > hasValidHitInFirstPixelBarrel(new std::vector<bool>());

  //-----------------------------------------------------------------
    edm::Handle<std::vector<reco::Track> > tracks;
    iEvent.getByLabel("generalTracks",tracks);

  if(tracks.isValid()) {
      for( std::vector<reco::Track>::const_iterator it = tracks->begin(); it != tracks->end(); ++it ) {
//          NDOF->push_back(it->ndof());
          Pt->push_back(it->pt());
//          PtError->push_back(it->ptError());
//          Px->push_back(it->px());
//          Py->push_back(it->py());
//          Pz->push_back(it->pz());
          Eta->push_back(it->eta());
//          EtaError->push_back(it->etaError());
          Phi->push_back(it->phi());
//          PhiError->push_back(it->phiError());
          Theta->push_back(it->theta());

          D0->push_back(it->d0());
//          D0Error->push_back(it->d0Error());
//          Dz->push_back(it->dz());
//          DzError->push_back(it->dzError());
          Vx->push_back(it->vx());
          Vy->push_back(it->vy());
          Vz->push_back(it->vz());

//          InnerPositionX->push_back(it->innerPosition().x());
//          InnerPositionY->push_back(it->innerPosition().y());
//          InnerPositionZ->push_back(it->innerPosition().z());
//          OuterPositionX->push_back(it->outerPosition().x());
//          OuterPositionY->push_back(it->outerPosition().y());
//          OuterPositionZ->push_back(it->outerPosition().z());

          Charge->push_back(it->charge());
//          recHitsSize->push_back(it->recHitsSize());
//          numberOfValidHits->push_back(it->numberOfValidHits());
//          numberOfLostHits->push_back(it->numberOfLostHits());
          innerLayerMissingHits->push_back(it->trackerExpectedHitsInner().numberOfHits());
//          innerLayerMissingHitsPixels->push_back(it->trackerExpectedHitsInner().numberOfValidPixelHits());
//          numPixelHits->push_back(it->hitPattern().numberOfValidPixelHits());
//          numStripHits->push_back(it->hitPattern().numberOfValidStripHits());

          isHighPurity->push_back(it->quality(reco::Track::highPurity));
//          hasValidHitInFirstPixelBarrel->push_back(it->hitPattern().hasValidHitInFirstPixelBarrel());
      }
  } else {
    edm::LogError("BristolNTuple_TrackError") << "Error! Can't get the product " << "generalTracks";
  }

  //-----------------------------------------------------------------
  // put vectors in the event

//  iEvent.put(NDOF , (prefix + "NDOF" + suffix));
  iEvent.put(Charge , (prefix + "Charge" + suffix));
  iEvent.put(Pt , (prefix + "Pt" + suffix));
//  iEvent.put(PtError , (prefix + "PtError" + suffix));
//  iEvent.put(Px , (prefix + "Px" + suffix));
//  iEvent.put(Py , (prefix + "Py" + suffix));
//  iEvent.put(Pz , (prefix + "Pz" + suffix));
  iEvent.put(Eta , (prefix + "Eta" + suffix));
//  iEvent.put(EtaError , (prefix + "EtaError" + suffix));
  iEvent.put(Phi , (prefix + "Phi" + suffix));
//  iEvent.put(PhiError , (prefix + "PhiError" + suffix));
  iEvent.put(Theta , (prefix + "Theta" + suffix));
  iEvent.put(D0 , (prefix + "D0" + suffix));
//  iEvent.put(D0Error , (prefix + "D0Error" + suffix));

//  iEvent.put(Dz , (prefix + "Dz" + suffix));
//  iEvent.put(DzError , (prefix + "DzError" + suffix));
  iEvent.put(Vx , (prefix + "Vx" + suffix));
  iEvent.put(Vy , (prefix + "Vy" + suffix));
  iEvent.put(Vz , (prefix + "Vz" + suffix));

//  iEvent.put(InnerPositionX , (prefix + "InnerPosition.x" + suffix));
//  iEvent.put(InnerPositionY , (prefix + "InnerPosition.y" + suffix));
//  iEvent.put(InnerPositionZ , (prefix + "InnerPosition.z" + suffix));
//  iEvent.put(OuterPositionX , (prefix + "OuterPosition.x" + suffix));
//  iEvent.put(OuterPositionY , (prefix + "OuterPosition.y" + suffix));
//  iEvent.put(OuterPositionZ , (prefix + "OuterPosition.z" + suffix));
//
//  iEvent.put(recHitsSize , (prefix + "recHitsSize" + suffix));
//  iEvent.put(numberOfValidHits , (prefix + "numberOfValidHits" + suffix));
//  iEvent.put(numberOfLostHits , (prefix + "numberOfLostHits" + suffix));
  iEvent.put(innerLayerMissingHits , (prefix + "innerLayerMissingHits" + suffix));
//  iEvent.put(innerLayerMissingHitsPixels , (prefix + "innerLayerMissingHitsPixels" + suffix));
//  iEvent.put(numPixelHits , (prefix + "numPixelHits" + suffix));
//  iEvent.put(numStripHits , (prefix + "numStripHits" + suffix));

  iEvent.put(isHighPurity , (prefix + "isHighPurity" + suffix));
//  iEvent.put(hasValidHitInFirstPixelBarrel , (prefix + "hasValidHitInFirstPixelBarrel" + suffix));

}

