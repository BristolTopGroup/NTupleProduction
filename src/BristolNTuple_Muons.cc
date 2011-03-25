#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Muons.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"


BristolNTuple_Muons::BristolNTuple_Muons(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
//    inputTagPVWithBS(iConfig.getParameter<edm::InputTag>("InputTagPVWithBS")),
//    inputTagBS(iConfig.getParameter<edm::InputTag>("InputTagBS")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize")),
    storePFIsolation (iConfig.getParameter<bool>    ("storePFIsolation"))
//    vtxInputTag(iConfig.getParameter<edm::InputTag>("VertexInputTag"))
{
  produces <std::vector<double> > ( prefix + "Px" + suffix );
  produces <std::vector<double> > ( prefix + "Py" + suffix );
  produces <std::vector<double> > ( prefix + "Pz" + suffix );
  produces <std::vector<double> > ( prefix + "TrkIso03" + suffix );
  produces <std::vector<double> > ( prefix + "EcalIso03" + suffix );
  produces <std::vector<double> > ( prefix + "HcalIso03" + suffix );
//  produces <std::vector<double> > ( prefix + "d0PVWithBS" + suffix );
//  produces <std::vector<double> > ( prefix + "d0BS" + suffix );
  produces <std::vector<int> >    ( prefix + "isGoodGlobalMuon" + suffix );
  if (storePFIsolation) {
        produces<std::vector<double> > (prefix + "PfChargedHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PfNeutralHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PFGammaIso" + suffix);
    }

}

void BristolNTuple_Muons::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  std::auto_ptr<std::vector<double> >  px  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  py  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  pz  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  trkIso03   ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  ecalIso03  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  hcalIso03  ( new std::vector<double>()  );
//  std::auto_ptr<std::vector<double> >  d0PVWithBS  ( new std::vector<double>()  );
//  std::auto_ptr<std::vector<double> >  d0BS  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<int> >     isGoodGlobalMuon  ( new std::vector<int>()  );
  std::auto_ptr<std::vector<double> >  PfChargedHadronIso  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  PfNeutralHadronIso  ( new std::vector<double>()  );
  std::auto_ptr<std::vector<double> >  PFGammaIso  ( new std::vector<double>()  );

  //-----------------------------------------------------------------
  edm::Handle < std::vector<pat::Muon> > muons;
  iEvent.getByLabel(inputTag, muons);

//  edm::Handle < std::vector<pat::Muon> > muonsWithBS;
//  iEvent.getByLabel(inputTagPVWithBS, muonsWithBS);
//
//  edm::Handle < std::vector<pat::Muon> > muonsBS;
//  iEvent.getByLabel(inputTagBS, muonsBS);

  edm::Handle<reco::VertexCollection> primaryVertices;
  iEvent.getByLabel("offlinePrimaryVerticesWithBS",primaryVertices);

  if(muons.isValid()) {
    edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muons->size();

    for( std::vector<pat::Muon>::const_iterator it = muons->begin(); it != muons->end(); ++it ) {
      // exit from loop when you reach the required number of muons
      if(px->size() >= maxSize)
        break;

      // if muon is not global muon, continue
      if(!it->isGlobalMuon())
        continue;

      px->push_back( it->px() );
      py->push_back( it->py() );
      pz->push_back( it->pz() );
      trkIso03->push_back( it->isolationR03().sumPt );
      ecalIso03->push_back( it->isolationR03().emEt );
      hcalIso03->push_back( it->isolationR03().hadEt );
      isGoodGlobalMuon->push_back( (it->isGood("AllGlobalMuons")) ? 1 : 0 );
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
              edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit " << "PfChargedHadronIsolation";
          if(PfNeutralHadronIsolation)
              PfNeutralHadronIso->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
          else
              edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit " << "PfNeutralHadronIsolation";
          if(PFGammaIsolation)
              PFGammaIso->push_back(PFGammaIsolation->depositWithin(0.3));
          else
              edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit " << "PFGammaIsolation";

//          delete PfChargedHadronIsolation;
//          delete PfNeutralHadronIsolation;
//          delete PFGammaIsolation;
      }
    }
  } else {
    edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the product " << inputTag;
  }

//  if(muonsWithBS.isValid()) {
//      edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muonsWithBS->size();
//
//      for( std::vector<pat::Muon>::const_iterator it = muonsWithBS->begin(); it != muonsWithBS->end(); ++it ) {
//        // exit from loop when you reach the required number of muons
//        if(d0PVWithBS->size() >= maxSize)
//          break;
//
//        // if muon is not global muon, continue
//        if(!it->isGlobalMuon())
//          continue;
//
//        double trkd0 = it->track()->d0();
//        d0PVWithBS->push_back(trkd0);
//
//      }
//    } else {
//      edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the product " << inputTag;
//    }
//
//  if(muonsBS.isValid()) {
//       edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muonsBS->size();
//
//       for( std::vector<pat::Muon>::const_iterator it = muonsBS->begin(); it != muonsBS->end(); ++it ) {
//         // exit from loop when you reach the required number of muons
//         if(d0BS->size() >= maxSize)
//           break;
//
//         // if muon is not global muon, continue
//         if(!it->isGlobalMuon())
//           continue;
//
//         double trkd0 = it->track()->d0();
//         d0BS->push_back(trkd0);
//
//       }
//     } else {
//       edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the product " << inputTag;
//     }

  //-----------------------------------------------------------------
  // put vectors in the event
  iEvent.put( px, prefix + "Px" + suffix );
  iEvent.put( py, prefix + "Py" + suffix );
  iEvent.put( pz, prefix + "Pz" + suffix );
  iEvent.put( trkIso03, prefix + "TrkIso03" + suffix );
  iEvent.put( ecalIso03, prefix + "EcalIso03" + suffix );
  iEvent.put( hcalIso03, prefix + "HcalIso03" + suffix );
//  iEvent.put( d0PVWithBS, prefix + "d0PVWithBS" + suffix );
//  iEvent.put( d0BS, prefix + "d0BS" + suffix );
  iEvent.put( isGoodGlobalMuon, prefix + "isGoodGlobalMuon" + suffix );
  if(storePFIsolation){
      iEvent.put( PfChargedHadronIso, prefix + "PfChargedHadronIso" + suffix );
      iEvent.put( PfNeutralHadronIso, prefix + "PfNeutralHadronIso" + suffix );
      iEvent.put( PFGammaIso, prefix + "PFGammaIso" + suffix );
  }
}
