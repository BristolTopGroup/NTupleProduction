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
    muonID  (iConfig.getParameter<std::string>  ("MuonID")),
    beamSpotCorr (iConfig.getParameter<bool>    ("BeamSpotCorr")),
    storePFIsolation(iConfig.getParameter<bool> ("storePFIsolation")),
    useCocktailRefits ( iConfig.getParameter<bool>("UseCocktailRefits")),
    vtxInputTag(iConfig.getParameter<edm::InputTag> ("VertexInputTag")) {

	//kinematic variables
    produces < std::vector<double> > (prefix + "Px" + suffix);
	produces < std::vector<double> > (prefix + "Py" + suffix);
	produces < std::vector<double> > (prefix + "Pz" + suffix);
	produces < std::vector<double> > (prefix + "Energy" + suffix);
	//extra properties
	produces < std::vector<int> > (prefix + "Charge" + suffix);

	//muon ID variables
	produces < std::vector<bool> > (prefix + "isGlobalMuon" + suffix);
	produces < std::vector<bool> > (prefix + "isTrackerMuon" + suffix);
	produces < std::vector<int> > (prefix + "NumberOfMatches" + suffix); // in reference selection
	produces < std::vector<int> > (prefix + "NumberOfMatchedStations" + suffix); // in Aachen selection
	produces < std::vector<double> > (prefix + "CosmicCompatibility" + suffix);
	produces < std::vector<double> > (prefix + "TimeCompatibility" + suffix);
	produces < std::vector<double> > (prefix + "BackToBackCompatibility" + suffix);
	produces < std::vector<double> > (prefix + "OverlapCompatibility" + suffix);
	produces <std::vector<bool> >    ( prefix + "PassID" + suffix );

	//muon isolation variables

	//default
	produces < std::vector<double> > (prefix + "TrkIso03" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "HOIso03" + suffix);
	//bigger cone
	produces < std::vector<double> > (prefix + "TrkIso05" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso05" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso05" + suffix);
	produces < std::vector<double> > (prefix + "HOIso05" + suffix);

	//muonn PF isolation variables
	if (storePFIsolation) {
		produces < std::vector<double> > (prefix + "PfChargedHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso03" + suffix);

		produces < std::vector<double> > (prefix + "PfChargedHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso04" + suffix);

		produces < std::vector<double> > (prefix + "PfChargedHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso05" + suffix);
	}

	//associated track
	produces < std::vector<double> > (prefix + "Track.D0" + suffix);
	produces < std::vector<double> > (prefix + "Track.D0Error" + suffix);
	produces < std::vector<double> > (prefix + "Track.Dz" + suffix);
	produces < std::vector<double> > (prefix + "Track.DzError" + suffix);
	produces < std::vector<double> > (prefix + "Track.ValidFractionOfHits" + suffix);


	//associated global track
	produces < std::vector<int> > (prefix + "GlobalTrack.NumberOfValidMuonHits" + suffix); // in reference selection
	produces < std::vector<double> > (prefix + "GlobalTrack.NormalizedChi2" + suffix); // in reference selection

	//associated inner track
	produces < std::vector<int> > (prefix + "InnerTrack.NumberOfValidHits" + suffix); // in reference selection (n Tracker Hits)
	produces < std::vector<int> > (prefix + "InnerTrack.PixelLayersWithMeasurement" + suffix); // in reference selection

	//muon vertex variables
	produces < std::vector<int> > (prefix + "Vertex.Index" + suffix);
	produces < std::vector<double> > (prefix + "Vertex.DistZ" + suffix); // in reference selection
	produces < std::vector<double> > (prefix + "PrimaryVertexDXY" + suffix); // in reference selection
	produces < std::vector<double> > (prefix + "PrimaryVertexDXYError" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXY" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXYError" + suffix);

	if (useCocktailRefits) {
		//muon cocktail variables
		produces < std::vector<double> > (prefix + "Cocktail.Px" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.Py" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.Pz" + suffix);
		produces < std::vector<int> > (prefix + "Cocktail.Charge" + suffix);
		produces < std::vector<int> > (prefix + "Cocktail.NumberOfValidTrackerHits" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.D0" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.D0Error" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.Dz" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.DzError" + suffix);
		produces < std::vector<double> > (prefix + "Cocktail.NormalizedChi2" + suffix);
	}

}

void BristolNTuple_Muons::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	//kinematic variables
	std::auto_ptr < std::vector<double> > px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy(new std::vector<double>());

	//extra properties
	std::auto_ptr < std::vector<int> > charge(new std::vector<int>());

	//muon ID variables
	std::auto_ptr < std::vector<bool> > isGlobalMuon(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > isTrackerMuon(new std::vector<bool>());
	std::auto_ptr < std::vector<int> > numberOfMatches(new std::vector<int>());
	std::auto_ptr < std::vector<int> > numberOfMatchedStations(new std::vector<int>());
	std::auto_ptr < std::vector<double> > cosmicCompatibility(new std::vector<double>());
	std::auto_ptr < std::vector<double> > timeCompatibility(new std::vector<double>());
	std::auto_ptr < std::vector<double> > backToBackCompatibility(new std::vector<double>());
	std::auto_ptr < std::vector<double> > overlapCompatibility(new std::vector<double>());
	std::auto_ptr < std::vector<bool> > passID(new std::vector<bool>());

	//muon isolation variables
	//default
	std::auto_ptr < std::vector<double> > trkIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIso03(new std::vector<double>());
	std::auto_ptr<std::vector<double> >  hoIso03    ( new std::vector<double>()  );
	//bigger cone
	std::auto_ptr < std::vector<double> > trkIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIso05(new std::vector<double>());
	std::auto_ptr<std::vector<double> >  hoIso05    ( new std::vector<double>()  );

	//muonn PF isolation variables
	std::auto_ptr < std::vector<double> > PfChargedHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso03(new std::vector<double>());

	std::auto_ptr < std::vector<double> > PfChargedHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso04(new std::vector<double>());

	std::auto_ptr < std::vector<double> > PfChargedHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso05(new std::vector<double>());

	//associated track
	std::auto_ptr < std::vector<double> > trkD0(new std::vector<double>());
	std::auto_ptr < std::vector<double> > trkD0Error(new std::vector<double>());
	std::auto_ptr < std::vector<double> > trkDz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > trkDzError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trackValidFractionOfHits(new std::vector<double>());

    //associated global track
    std::auto_ptr < std::vector<int> > globalTrackNumberOfValidMuonHits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > globalChi2(new std::vector<double>());

    //associated inner track
    std::auto_ptr < std::vector<int> > innerTrackNumberOfValidHits(new std::vector<int>());
    std::auto_ptr < std::vector<int> > innerTrackPixelLayersWithMeasurement(new std::vector<int>());

    //muon vertex variables
    std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
    std::auto_ptr<std::vector<double> >  vtxDistZ  ( new std::vector<double>()  );
    std::auto_ptr < std::vector<double> > primaryVertexDXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > primaryVertexDXYError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamSpotDXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamSpotDXYError(new std::vector<double>());

    //muon cocktail variables
    std::auto_ptr < std::vector<double> > ctPx(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctPy(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctPz(new std::vector<double>());
    std::auto_ptr < std::vector<int> > ctCharge(new std::vector<int>());
    std::auto_ptr < std::vector<int> > ctNumberOfValidTrackerHits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > ctTrkD0(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkD0Error(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkDz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctTrkDzError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ctNormalizedChi2(new std::vector<double>());

    //-----------------------------------------------------------------
    edm::Handle < std::vector<pat::Muon> > muons;
    iEvent.getByLabel(inputTag, muons);

    edm::Handle < reco::VertexCollection > primaryVertices;
    iEvent.getByLabel(vtxInputTag, primaryVertices);

    edm::Handle < reco::BeamSpot > beamSpot;
	iEvent.getByLabel("offlineBeamSpot", beamSpot);

    if (muons.isValid()) {
        edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muons->size();

        for (std::vector<pat::Muon>::const_iterator it = muons->begin(); it != muons->end(); ++it) {
            // exit from loop when you reach the required number of muons
            if (px->size() >= maxSize)
                break;
            if (!it->isGlobalMuon())
                continue;

            double trkd0 = it->track()->d0();

            if (beamSpotCorr && beamSpot.isValid()) {
				trkd0 = -(it->track()->dxy(beamSpot->position()));
			}
			else if (beamSpotCorr && !beamSpot.isValid())
				edm::LogError("RootTupleMakerV2_MuonsError") << "Error! Can't get the offlineBeamSpot";


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

            //kinematic variables
            px->push_back(it->px());
            py->push_back(it->py());
            pz->push_back(it->pz());
            energy->push_back(it->energy());
            //extra properties
            charge->push_back(it->charge());

            //muon ID variables
            isGlobalMuon->push_back(it->isGlobalMuon());
			isTrackerMuon->push_back(it->isTrackerMuon());
			numberOfMatches->push_back(it->numberOfMatches());
			numberOfMatchedStations->push_back(it->numberOfMatchedStations());
			cosmicCompatibility->push_back(it->userFloat("cosmicCompatibility"));
			timeCompatibility->push_back(it->userFloat("timeCompatibility"));
			backToBackCompatibility->push_back(it->userFloat("backToBackCompatibility"));
			overlapCompatibility->push_back(it->userFloat("overlapCompatibility"));
			passID->push_back(it->muonID(muonID));


			//muon isolation variables
			//default
			trkIso03->push_back(it->isolationR03().sumPt);
			ecalIso03->push_back(it->isolationR03().emEt);
			hcalIso03->push_back(it->isolationR03().hadEt);
			hoIso03->push_back( it->isolationR03().hoEt );
			//bigger cone
			trkIso05->push_back(it->isolationR05().sumPt);
			ecalIso05->push_back(it->isolationR05().emEt);
			hcalIso05->push_back(it->isolationR05().hadEt);
			hoIso05->push_back( it->isolationR05().hoEt );

            if (storePFIsolation) {
                pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
				pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
				pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);

				const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
				const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
				const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
				if (PfChargedHadronIsolation) {
					PfChargedHadronIso03->push_back(PfChargedHadronIsolation->depositWithin(0.3));
					PfChargedHadronIso04->push_back(PfChargedHadronIsolation->depositWithin(0.4));
					PfChargedHadronIso05->push_back(PfChargedHadronIsolation->depositWithin(0.5));
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfChargedHadronIsolation";
				if (PfNeutralHadronIsolation) {
					PfNeutralHadronIso03->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
					PfNeutralHadronIso04->push_back(PfNeutralHadronIsolation->depositWithin(0.4));
					PfNeutralHadronIso05->push_back(PfNeutralHadronIsolation->depositWithin(0.5));
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfNeutralHadronIsolation";
				if (PFGammaIsolation) {
					PFGammaIso03->push_back(PFGammaIsolation->depositWithin(0.3));
					PFGammaIso04->push_back(PFGammaIsolation->depositWithin(0.4));
					PFGammaIso05->push_back(PFGammaIsolation->depositWithin(0.5));
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PFGammaIsolation";

            }

            //associated track
            trkD0->push_back(trkd0);
			trkD0Error->push_back(it->track()->d0Error());
			trkDz->push_back(it->track()->dz());
			trkDzError->push_back(it->track()->dzError());
			trackValidFractionOfHits->push_back (  validFraction ( it->track() ));


			//associated global track
            globalChi2->push_back(it->globalTrack()->normalizedChi2());
            globalTrackNumberOfValidMuonHits->push_back(it->globalTrack()->hitPattern().numberOfValidMuonHits());

            //associated inner track
            innerTrackNumberOfValidHits->push_back( it->innerTrack()->numberOfValidHits() );
            innerTrackPixelLayersWithMeasurement->push_back( it->innerTrack()->hitPattern().pixelLayersWithMeasurement() );

            //muon vertex variables
            vtxIndex->push_back(vtxIndex_);
			vtxDistZ->push_back(vtxDistZ_);
			primaryVertexDXY->push_back(it->dB());
			primaryVertexDXYError->push_back(it->edB());
			beamSpotDXY->push_back(it->dB(pat::Muon::BS2D));
			beamSpotDXYError->push_back(it->edB(pat::Muon::BS2D));

			if (useCocktailRefits) {
				int refit_id = -999;
				const reco::TrackRef& cocktail_track = pmcTrack(*it, refit_id);

				double cttrkd0 = cocktail_track->d0();

				if (beamSpotCorr && beamSpot.isValid())
					cttrkd0 = -(cocktail_track->dxy(beamSpot->position()));

				ctPx->push_back(cocktail_track->px());
				ctPy->push_back(cocktail_track->py());
				ctPz->push_back(cocktail_track->pz());
				ctCharge->push_back(cocktail_track->charge());
				ctNumberOfValidTrackerHits->push_back(cocktail_track->numberOfValidHits());
				ctTrkD0->push_back(cttrkd0);
				ctTrkD0Error->push_back(cocktail_track->d0Error());
				ctTrkDz->push_back(cocktail_track->dz());
				ctTrkDzError->push_back(cocktail_track->dzError());
				ctNormalizedChi2->push_back(cocktail_track->normalizedChi2());
			}



        }
    } else {
        edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the product " << inputTag;
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    //kinematic variables
    iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put( energy, prefix + "Energy" + suffix );

    //extra properties
    iEvent.put( charge, prefix + "Charge" + suffix );

    //muon ID variables
    iEvent.put( isGlobalMuon, prefix + "isGlobalMuon" + suffix );
    iEvent.put( isTrackerMuon, prefix + "isTrackerMuon" + suffix );
    iEvent.put( numberOfMatches, prefix + "NumberOfMatches" + suffix );
    iEvent.put( numberOfMatchedStations, prefix + "NumberOfMatchedStations" + suffix );
    iEvent.put( cosmicCompatibility, prefix + "CosmicCompatibility" + suffix );
    iEvent.put( timeCompatibility, prefix + "TimeCompatibility" + suffix );
    iEvent.put( backToBackCompatibility, prefix + "BackToBackCompatibility" + suffix );
    iEvent.put( overlapCompatibility, prefix + "OverlapCompatibility" + suffix );
    iEvent.put( passID, prefix + "PassID" + suffix );


    //muon isolation variables
    //default
    iEvent.put(trkIso03, prefix + "TrkIso03" + suffix);
    iEvent.put(ecalIso03, prefix + "EcalIso03" + suffix);
    iEvent.put(hcalIso03, prefix + "HcalIso03" + suffix);
    iEvent.put(hoIso03, prefix + "HOIso03" + suffix);
    //bigger cone
    iEvent.put(trkIso05, prefix + "TrkIso05" + suffix);
	iEvent.put(ecalIso05, prefix + "EcalIso05" + suffix);
	iEvent.put(hcalIso05, prefix + "HcalIso05" + suffix);
	iEvent.put(hoIso05, prefix + "HOIso05" + suffix);

	//muon PF isolation variables
	if (storePFIsolation) {
		iEvent.put(PfChargedHadronIso03, prefix + "PfChargedHadronIso03" + suffix);
		iEvent.put(PfNeutralHadronIso03, prefix + "PfNeutralHadronIso03" + suffix);
		iEvent.put(PFGammaIso03, prefix + "PFGammaIso03" + suffix);

		iEvent.put(PfChargedHadronIso04, prefix + "PfChargedHadronIso04" + suffix);
		iEvent.put(PfNeutralHadronIso04, prefix + "PfNeutralHadronIso04" + suffix);
		iEvent.put(PFGammaIso04, prefix + "PFGammaIso04" + suffix);

		iEvent.put(PfChargedHadronIso05, prefix + "PfChargedHadronIso05" + suffix);
		iEvent.put(PfNeutralHadronIso05, prefix + "PfNeutralHadronIso05" + suffix);
		iEvent.put(PFGammaIso05, prefix + "PFGammaIso05" + suffix);
	}

	//associated track
	iEvent.put(trkD0, prefix + "Track.D0" + suffix);
	iEvent.put(trkD0Error, prefix + "Track.D0Error" + suffix);
	iEvent.put(trkDz, prefix + "Track.Dz" + suffix);
	iEvent.put(trkDzError, prefix + "Track.DzError" + suffix);
	iEvent.put(trackValidFractionOfHits, prefix + "Track.ValidFractionOfHits" + suffix);

	//associated global track
	iEvent.put(globalTrackNumberOfValidMuonHits, prefix + "GlobalTrack.NumberOfValidMuonHits" + suffix);
	iEvent.put(globalChi2, prefix + "GlobalTrack.NormalizedChi2" + suffix);

	//associated inner track
	iEvent.put(innerTrackNumberOfValidHits, prefix + "InnerTrack.NumberOfValidHits" + suffix);
	iEvent.put(innerTrackPixelLayersWithMeasurement, prefix + "InnerTrack.PixelLayersWithMeasurement" + suffix);

	//muon vertex variables
	iEvent.put(vtxIndex, prefix + "VtxIndex" + suffix);
	iEvent.put(vtxDistZ, prefix + "VtxDistZ" + suffix);

	iEvent.put(primaryVertexDXY, prefix + "PrimaryVertexDXY" + suffix);
	iEvent.put(primaryVertexDXYError, prefix + "PrimaryVertexDXYError" + suffix);
	iEvent.put(beamSpotDXY, prefix + "BeamSpotDXY" + suffix);
	iEvent.put(beamSpotDXYError, prefix + "BeamSpotDXYError" + suffix);

	if (useCocktailRefits) {
		iEvent.put(ctPx, prefix + "Cocktail.Px" + suffix);
		iEvent.put(ctPy, prefix + "Cocktail.Py" + suffix);
		iEvent.put(ctPz, prefix + "Cocktail.Pz" + suffix);
		iEvent.put(ctCharge, prefix + "Cocktail.Charge" + suffix);
		iEvent.put(ctNumberOfValidTrackerHits, prefix + "Cocktail.NumberOfValidTrackerHits" + suffix);
		iEvent.put(ctTrkD0, prefix + "Cocktail.D0" + suffix);
		iEvent.put(ctTrkD0Error, prefix + "Cocktail.D0Error" + suffix);
		iEvent.put(ctTrkDz, prefix + "Cocktail.Dz" + suffix);
		iEvent.put(ctTrkDzError, prefix + "Cocktail.DzError" + suffix);
		iEvent.put(ctNormalizedChi2, prefix + "Cocktail.NormalizedChi2" + suffix);
	}
}
