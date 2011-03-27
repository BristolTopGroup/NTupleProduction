#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_EventSelection.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GtFdlWord.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/METReco/interface/HcalNoiseSummary.h"


BristolNTuple_EventSelection::BristolNTuple_EventSelection(const edm::ParameterSet& iConfig) :
    l1InputTag(iConfig.getParameter<edm::InputTag>("L1InputTag")),
    vtxInputTag(iConfig.getParameter<edm::InputTag>("VertexInputTag")),
    vtxMinNDOF(iConfig.getParameter<unsigned int>("VertexMinimumNDOF")),
    vtxMaxAbsZ(iConfig.getParameter<double>("VertexMaxAbsZ")),
    vtxMaxd0(iConfig.getParameter<double>("VertexMaxd0")),
    trkInputTag(iConfig.getParameter<edm::InputTag>("TracksInputTag")),
    numTracks(iConfig.getParameter<unsigned int>("NumTracks")),
    hpTrackThreshold(iConfig.getParameter<double>("HPTrackThreshold")),
    hcalNoiseInputTag(iConfig.getParameter<edm::InputTag>("HcalNoiseInputTag")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix"))
{
  produces <bool> (prefix + "hasPhysDeclared" + suffix);
  produces <bool> (prefix + "isBPTX0" + suffix);
  produces <bool> (prefix + "isBSCMinBias" + suffix);
  produces <bool> (prefix + "isBSCBeamHalo" + suffix);
  produces <bool> (prefix + "hasGoodPrimaryVertex" + suffix);
  produces <bool> (prefix + "isBeamScraping" + suffix);
  produces <bool> (prefix + "passesHBHENoiseFilter" + suffix);
}

void BristolNTuple_EventSelection::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  std::auto_ptr<bool> isphysdeclared( new bool() );
  std::auto_ptr<bool> isbptx0( new bool() );
  std::auto_ptr<bool> isbscminbias( new bool() );
  std::auto_ptr<bool> isbscbeamhalo( new bool() );
  std::auto_ptr<bool> isprimaryvertex( new bool() );
  std::auto_ptr<bool> isbeamscraping( new bool() );
  std::auto_ptr<bool> passhbhenoisefilter( new bool() );


  *isphysdeclared.get() = false;
  *isbptx0.get() = false;
  *isbscminbias.get() = false;
  *isbscbeamhalo.get() = false;
  *isprimaryvertex.get() = false;
  *isbeamscraping.get() = false;
  *passhbhenoisefilter.get() = true;

  //-----------------------------------------------------------------
  edm::Handle<L1GlobalTriggerReadoutRecord> l1GtReadoutRecord;
  iEvent.getByLabel(l1InputTag, l1GtReadoutRecord);

  // Technical Trigger Part
  if(l1GtReadoutRecord.isValid()) {
    edm::LogInfo("BristolNTuple_EventSelectionInfo") << "Successfully obtained " << l1InputTag;

    L1GtFdlWord fdlWord = l1GtReadoutRecord->gtFdlWord();
    if (fdlWord.physicsDeclared() == 1)
      *isphysdeclared.get() = true;

    // BPTX0
    if ( l1GtReadoutRecord->technicalTriggerWord()[0] )
      *isbptx0.get() = true;

    // MinBias
    if ( l1GtReadoutRecord->technicalTriggerWord()[40] || l1GtReadoutRecord->technicalTriggerWord()[41] )
      *isbscminbias.get() = true;

    // BeamHalo
    if ( (l1GtReadoutRecord->technicalTriggerWord()[36] || l1GtReadoutRecord->technicalTriggerWord()[37] ||
          l1GtReadoutRecord->technicalTriggerWord()[38] || l1GtReadoutRecord->technicalTriggerWord()[39]) ||
         ((l1GtReadoutRecord->technicalTriggerWord()[42] && !l1GtReadoutRecord->technicalTriggerWord()[43]) ||
          (l1GtReadoutRecord->technicalTriggerWord()[43] && !l1GtReadoutRecord->technicalTriggerWord()[42])) )
      *isbscbeamhalo.get() = true;

  } else {
    edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << l1InputTag;
  }

  // Good Primary Vertex Part
  edm::Handle<reco::VertexCollection> primaryVertices;
  iEvent.getByLabel(vtxInputTag,primaryVertices);

  if(primaryVertices.isValid()) {
    edm::LogInfo("BristolNTuple_EventSelectionInfo") << "Total # Primary Vertices: " << primaryVertices->size();

    for( reco::VertexCollection::const_iterator it=primaryVertices->begin() ; it!=primaryVertices->end() ; ++it ) {
      if( !(it->isFake()) && it->ndof() > vtxMinNDOF &&
          fabs(it->z()) <= vtxMaxAbsZ && fabs(it->position().rho()) <= vtxMaxd0
        ) *isprimaryvertex.get() = true;
    }
  } else {
    edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << vtxInputTag;
  }

  // Scraping Events Part
  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByLabel(trkInputTag,tracks);

  if(tracks.isValid()) {
    edm::LogInfo("BristolNTuple_EventSelectionInfo") << "Total # Tracks: " << tracks->size();

    int numhighpurity = 0;
    double fraction = 1.;
    reco::TrackBase::TrackQuality trackQuality = reco::TrackBase::qualityByName("highPurity");

    if( tracks->size() > numTracks ){
      for( reco::TrackCollection::const_iterator it=tracks->begin(); it!=tracks->end(); ++it ) {
        if( it->quality(trackQuality) ) numhighpurity++;
      }
      fraction = (double)numhighpurity/(double)tracks->size();
      if( fraction < hpTrackThreshold ) *isbeamscraping.get() = true;
    }
  } else {
    edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << trkInputTag;
  }

  // Hcal Noise Part
  edm::Handle<bool> hbheFilterResult;
  iEvent.getByLabel(hcalNoiseInputTag, hbheFilterResult);

  if(hbheFilterResult.isValid()) {
    edm::LogInfo("BristolNTuple_EventSelectionInfo") << "Successfully obtained " << hcalNoiseInputTag;

      *passhbhenoisefilter.get()=*hbheFilterResult;
  } else {
    edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << hcalNoiseInputTag;
  }

  //-----------------------------------------------------------------
    iEvent.put(isphysdeclared, prefix + "hasPhysDeclared" + suffix);
    iEvent.put(isbptx0, prefix + "isBPTX0" + suffix);
    iEvent.put(isbscminbias, prefix + "isBSCMinBias" + suffix);
    iEvent.put(isbscbeamhalo, prefix + "isBSCBeamHalo" + suffix);
    iEvent.put(isprimaryvertex, prefix + "hasGoodPrimaryVertex" + suffix);
    iEvent.put(isbeamscraping, prefix + "isBeamScraping" + suffix);
    iEvent.put(passhbhenoisefilter, prefix + "passesHBHENoiseFilter" + suffix);
}
