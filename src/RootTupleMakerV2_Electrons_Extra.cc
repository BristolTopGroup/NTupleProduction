#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Electrons_Extra.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

RootTupleMakerV2_Electrons_Extra::RootTupleMakerV2_Electrons_Extra(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
    inputTagPVWithBS(iConfig.getParameter<edm::InputTag>("InputTagPVWithBS")),
    inputTagBS(iConfig.getParameter<edm::InputTag>("InputTagBS")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize")),
    storePFIsolation (iConfig.getParameter<bool>    ("storePFIsolation"))
{
  produces <std::vector<double> > ( prefix + "Px" + suffix );
  produces <std::vector<double> > ( prefix + "Py" + suffix );
  produces <std::vector<double> > ( prefix + "Pz" + suffix );
  produces <std::vector<double> > ( prefix + "TrkIso03" + suffix );
  produces <std::vector<double> > ( prefix + "EcalIso03" + suffix );
  produces <std::vector<double> > ( prefix + "HcalIso03" + suffix );
  produces <std::vector<double> > ( prefix + "dB" + suffix );
  produces <std::vector<double> > ( prefix + "dBPVWithBS" + suffix );
  produces <std::vector<double> > ( prefix + "dBBS" + suffix );

  produces <std::vector<int> > ( prefix + "closestCtfTrackRef" + suffix );
  produces <std::vector<double> > ( prefix + "shFracInnerHits" + suffix );
  produces <std::vector<double> > ( prefix + "GSFTrack.d0" + suffix );
  produces <std::vector<double> > ( prefix + "GSFTrack.Eta" + suffix );
  produces <std::vector<double> > ( prefix + "GSFTrack.Phi" + suffix );
  produces <std::vector<double> > ( prefix + "GSFTrack.Theta" + suffix );
  produces <std::vector<int> > ( prefix + "GSFTrack.Charge" + suffix );

  produces<std::vector<double> > (prefix + "Vertex.X" + suffix);
  produces<std::vector<double> > (prefix + "Vertex.Y" + suffix);
  produces<std::vector<double> > (prefix + "Vertex.Z" + suffix);

  produces<std::vector<double> > (prefix + "VertexWithBS.X" + suffix);
  produces<std::vector<double> > (prefix + "VertexWithBS.Y" + suffix);
  produces<std::vector<double> > (prefix + "VertexWithBS.Z" + suffix);

  produces<std::vector<double> > (prefix + "VertexBS.X" + suffix);
  produces<std::vector<double> > (prefix + "VertexBS.Y" + suffix);
  produces<std::vector<double> > (prefix + "VertexBS.Z" + suffix);

  if (storePFIsolation) {
        produces<std::vector<double> > (prefix + "PfChargedHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PfNeutralHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PFGammaIso" + suffix);
    }
}

void RootTupleMakerV2_Electrons_Extra::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  std::auto_ptr<std::vector<double> >  px  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  py  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  pz  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  trkIso03   ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  ecalIso03  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  hcalIso03  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  dB  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  dBPVWithBS  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  dBBS  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  PfChargedHadronIso  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  PfNeutralHadronIso  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  PFGammaIso  ( new std::vector<double>()  );

  std::auto_ptr<std::vector<int> >  closestCtfTrackRef  ( new std::vector<int>()  );
  std::auto_ptr<std::vector<double> >  shFracInnerHits  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  gsfTrackD0  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  gsfTrackEta  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  gsfTrackPhi  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  gsfTrackTheta  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<int> >  gsfTrackCharge  ( new std::vector<int>()  );

  std::auto_ptr<std::vector<double> >  VertexX  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexY  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexZ  ( new std::vector<double>()  );

  std::auto_ptr<std::vector<double> >  VertexWithBSX  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexWithBSY  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexWithBSZ  ( new std::vector<double>()  );

  std::auto_ptr<std::vector<double> >  VertexBSX  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexBSY  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  VertexBSZ  ( new std::vector<double>()  );

  //-----------------------------------------------------------------
  edm::Handle < std::vector<pat::Electron> > electrons;
  iEvent.getByLabel(inputTag, electrons);

  edm::Handle < std::vector<pat::Electron> > electronsWithBS;
  iEvent.getByLabel(inputTagPVWithBS, electronsWithBS);

  edm::Handle < std::vector<pat::Electron> > electronsBS;
  iEvent.getByLabel(inputTagBS, electronsBS);

//  edm::Handle<reco::VertexCollection> primaryVertices;
//  iEvent.getByLabel("offlinePrimaryVerticesWithBS",primaryVertices);

  if(electrons.isValid()) {
    edm::LogInfo("RootTupleMakerV2_ElectronsExtraInfo") << "Total # Electrons: " << electrons->size();
    for( std::vector<pat::Electron>::const_iterator it = electrons->begin(); it != electrons->end(); ++it ) {
      // exit from loop when you reach the required number of electrons
      if(px->size() >= maxSize)
        break;

      px->push_back( it->px() );
      py->push_back( it->py() );
      pz->push_back( it->pz() );
      trkIso03->push_back( it->dr03TkSumPt() );
      ecalIso03->push_back( it->dr03EcalRecHitSumEt());
      hcalIso03->push_back( it->dr03HcalTowerSumEt());
      closestCtfTrackRef->push_back(static_cast<int>(it->closestCtfTrackRef().key()));
      shFracInnerHits->push_back(it->shFracInnerHits());


      gsfTrackD0->push_back(it->gsfTrack()->d0());
      gsfTrackEta->push_back(it->gsfTrack()->eta());
      gsfTrackPhi->push_back(it->gsfTrack()->phi());
      gsfTrackTheta->push_back(it->gsfTrack()->theta());
      gsfTrackCharge->push_back(it->gsfTrack()->charge());
      dB->push_back(it->dB());

      VertexX->push_back(it->vertex().x());
      VertexY->push_back(it->vertex().y());
      VertexZ->push_back(it->vertex().z());

      if(storePFIsolation){
          pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
          pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
          pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);

          const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
          const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
          const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
          if(PfChargedHadronIsolation)
              PfChargedHadronIso->push_back(PfChargedHadronIsolation->depositWithin(0.3));
          else
              edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the isolation deposit "
              << "PfChargedHadronIsolation";
          if(PfNeutralHadronIsolation)
              PfNeutralHadronIso->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
          else
              edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the isolation deposit "
              << "PfNeutralHadronIsolation";
          if(PFGammaIsolation)
              PFGammaIso->push_back(PFGammaIsolation->depositWithin(0.3));
          else
              edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the isolation deposit "
              << "PFGammaIsolation";
      }


    }
  } else {
    edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the product " << inputTag;
  }

  if(electronsWithBS.isValid()) {
      edm::LogInfo("RootTupleMakerV2_ElectronsExtraInfo") << "Total # Electrons: " << electronsWithBS->size();
      for( std::vector<pat::Electron>::const_iterator it = electronsWithBS->begin(); it != electronsWithBS->end(); ++it ) {
        // exit from loop when you reach the required number of electrons
        if(dBPVWithBS->size() >= maxSize)
          break;

        dBPVWithBS->push_back(it->dB());

        VertexWithBSX->push_back(it->vertex().x());
        VertexWithBSY->push_back(it->vertex().y());
        VertexWithBSZ->push_back(it->vertex().z());

      }
    } else {
      edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the product " << inputTagPVWithBS;
    }

  if(electronsBS.isValid()) {
       edm::LogInfo("RootTupleMakerV2_ElectronsExtraInfo") << "Total # Electrons: " << electronsBS->size();
       for( std::vector<pat::Electron>::const_iterator it = electronsBS->begin(); it != electronsBS->end(); ++it ) {
         // exit from loop when you reach the required number of electrons
         if(dBBS->size() >= maxSize)
           break;

         dBBS->push_back(it->dB());

         VertexBSX->push_back(it->vertex().x());
         VertexBSY->push_back(it->vertex().y());
         VertexBSZ->push_back(it->vertex().z());

       }
     } else {
       edm::LogError("RootTupleMakerV2_ElectronsExtraError") << "Error! Can't get the product " << inputTagBS;
     }

  //-----------------------------------------------------------------
  // put vectors in the event
  iEvent.put( px, prefix + "Px" + suffix );
  iEvent.put( py, prefix + "Py" + suffix );
  iEvent.put( pz, prefix + "Pz" + suffix );
  iEvent.put( trkIso03, prefix + "TrkIso03" + suffix );
  iEvent.put( ecalIso03, prefix + "EcalIso03" + suffix );
  iEvent.put( hcalIso03, prefix + "HcalIso03" + suffix );
  iEvent.put( dB, prefix + "dB" + suffix );
  iEvent.put( dBPVWithBS, prefix + "dBPVWithBS" + suffix );
  iEvent.put( dBBS, prefix + "dBBS" + suffix );

  iEvent.put( closestCtfTrackRef, prefix + "closestCtfTrackRef" + suffix );
  iEvent.put( shFracInnerHits, prefix + "shFracInnerHits" + suffix );
  iEvent.put( gsfTrackD0, prefix + "GSFTrack.d0" + suffix );
  iEvent.put( gsfTrackEta, prefix + "GSFTrack.Eta" + suffix );
  iEvent.put( gsfTrackPhi, prefix + "GSFTrack.Phi" + suffix );
  iEvent.put( gsfTrackTheta, prefix + "GSFTrack.Theta" + suffix );
  iEvent.put( gsfTrackCharge, prefix + "GSFTrack.Charge" + suffix );

  iEvent.put( VertexX, prefix + "Vertex.X" + suffix );
  iEvent.put( VertexY, prefix + "Vertex.Y" + suffix );
  iEvent.put( VertexZ, prefix + "Vertex.Z" + suffix );

  iEvent.put( VertexWithBSX, prefix + "VertexWithBS.X" + suffix );
  iEvent.put( VertexWithBSY, prefix + "VertexWithBS.Y" + suffix );
  iEvent.put( VertexWithBSZ, prefix + "VertexWithBS.Z" + suffix );

  iEvent.put( VertexBSX, prefix + "VertexBS.X" + suffix );
  iEvent.put( VertexBSY, prefix + "VertexBS.Y" + suffix );
  iEvent.put( VertexBSZ, prefix + "VertexBS.Z" + suffix );

  if(storePFIsolation){
      iEvent.put( PfChargedHadronIso, prefix + "PfChargedHadronIso" + suffix );
      iEvent.put( PfNeutralHadronIso, prefix + "PfNeutralHadronIso" + suffix );
      iEvent.put( PFGammaIso, prefix + "PFGammaIso" + suffix );
  }
}
