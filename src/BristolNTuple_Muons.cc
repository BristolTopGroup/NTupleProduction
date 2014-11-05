#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Muons.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "BristolAnalysis/NTupleTools/interface/DirectionalIsolation.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"

BristolNTuple_Muons::BristolNTuple_Muons(const edm::ParameterSet& iConfig) :
		inputTag(iConfig.getParameter < edm::InputTag > ("InputTag")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")), //
		maxSize(iConfig.getParameter<unsigned int>("MaxSize")), //
		muonID(iConfig.getParameter < std::string > ("MuonID")), //
		beamSpotCorr(iConfig.getParameter<bool>("BeamSpotCorr")), //
		storePFIsolation(iConfig.getParameter<bool>("storePFIsolation")), //
		vtxInputTag(iConfig.getParameter < edm::InputTag > ("VertexInputTag")) //
{

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
	produces < std::vector<bool> > (prefix + "isPFMuon" + suffix);
	produces < std::vector<int> > (prefix + "NumberOfMatches" + suffix); // in reference selection
	produces < std::vector<int> > (prefix + "NumberOfMatchedStations" + suffix); // in Aachen selection
	produces < std::vector<bool> > (prefix + "PassID" + suffix);

	//muon isolation variables

	//default
	produces < std::vector<double> > (prefix + "TrkIso03" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "HOIso03" + suffix);
	produces < std::vector<double> > (prefix + "RelIso03" + suffix);
	//bigger cone
	produces < std::vector<double> > (prefix + "TrkIso05" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso05" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso05" + suffix);
	produces < std::vector<double> > (prefix + "HOIso05" + suffix);
	produces < std::vector<double> > (prefix + "RelIso05" + suffix);

	//muonn PF isolation variables
	if (storePFIsolation) {
		produces < std::vector<double> > (prefix + "PfChargedHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso03" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso03" + suffix);

		produces < std::vector<double> > (prefix + "PfChargedHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso04" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso04" + suffix);

		produces < std::vector<double> > (prefix + "PfChargedHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso05" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso05" + suffix);

		//directional isolation
		produces < std::vector<double> > (prefix + "DirectionalPFIso02" + suffix);
		produces < std::vector<double> > (prefix + "DirectionalPFIso02FallOff" + suffix);
		produces < std::vector<double> > (prefix + "PfRelIso02FallOff" + suffix);
		produces < std::vector<double> > (prefix + "DirectionalPFIso03" + suffix);
		produces < std::vector<double> > (prefix + "DirectionalPFIso03FallOff" + suffix);
		produces < std::vector<double> > (prefix + "PfRelIso03FallOff" + suffix);
		//PU charged hadron isolation
		produces < std::vector<double> > (prefix + "PfPUChargedHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PfPUChargedHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PfPUChargedHadronIso05" + suffix);
		
		//new variable for pf delta beta corrected reliso
		produces < std::vector<double> > (prefix + "sumChargedHadronPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumChargedHadronPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumNeutralHadronPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumNeutralHadronPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumPhotonPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumPhotonPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumPUPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumPUPt04" + suffix);
		
		produces < std::vector<double> > (prefix + "PFRelIso03DeltaBeta" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso04DeltaBeta" + suffix);
		
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
	produces < std::vector<int> > (prefix + "InnerTrack.TrackerLayersWithMeasurement" + suffix); // in reference selection
	produces < std::vector<int> > (prefix + "InnerTrack.NumberOfValidPixelHits" + suffix); // in reference selection

	//muon vertex variables
	produces < std::vector<int> > (prefix + "Vertex.Index" + suffix);
	produces < std::vector<double> > (prefix + "Vertex.DistZ" + suffix); // in reference selection
	produces < std::vector<double> > (prefix + "PrimaryVertexDXY" + suffix); // in reference selection
	produces < std::vector<double> > (prefix + "PrimaryVertexDXYError" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXY" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXYError" + suffix);
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
	std::auto_ptr < std::vector<bool> > isPFMuon(new std::vector<bool>());
	std::auto_ptr < std::vector<int> > numberOfMatches(new std::vector<int>());
	std::auto_ptr < std::vector<int> > numberOfMatchedStations(new std::vector<int>());
	std::auto_ptr < std::vector<bool> > passID(new std::vector<bool>());

	//muon isolation variables
	//default
	std::auto_ptr < std::vector<double> > trkIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hoIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > relIso03(new std::vector<double>());
	//bigger cone
	std::auto_ptr < std::vector<double> > trkIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hoIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > relIso05(new std::vector<double>());

	//muonn PF isolation variables
	std::auto_ptr < std::vector<double> > PfChargedHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso03(new std::vector<double>());

	std::auto_ptr < std::vector<double> > PfChargedHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso04(new std::vector<double>());


	std::auto_ptr < std::vector<double> > PfChargedHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso05(new std::vector<double>());

	std::auto_ptr < std::vector<double> > DirectionalPFIso02(new std::vector<double>());
	std::auto_ptr < std::vector<double> > DirectionalPFIso02FallOff(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfRelIso02FallOff(new std::vector<double>());
	std::auto_ptr < std::vector<double> > DirectionalPFIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > DirectionalPFIso03FallOff(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfRelIso03FallOff(new std::vector<double>());

	//PU charged hadron isolation
	std::auto_ptr < std::vector<double> > PfPUChargedHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfPUChargedHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfPUChargedHadronIso05(new std::vector<double>());
	
	//new iso vars
	std::auto_ptr < std::vector<double> > sumChargedHadronPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumChargedHadronPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumNeutralHadronPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumNeutralHadronPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPhotonPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPhotonPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPUPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPUPt04(new std::vector<double>());
	
	std::auto_ptr < std::vector<double> > PFRelIso03DeltaBeta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso04DeltaBeta(new std::vector<double>());
	
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
	std::auto_ptr < std::vector<int> > innerTrackTrackerLayersWithMeasurement(new std::vector<int>());
	std::auto_ptr < std::vector<int> > innerTrackNumberOfValidPixelHits(new std::vector<int>());

	//muon vertex variables
	std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
	std::auto_ptr < std::vector<double> > vtxDistZ(new std::vector<double>());
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

	edm::Handle < reco::PFCandidateCollection > pfCandidates;
	iEvent.getByLabel("particleFlow", pfCandidates);

	if (muons.isValid()) {
		edm::LogInfo("BristolNTuple_MuonsExtraInfo") << "Total # Muons: " << muons->size();

		for (std::vector<pat::Muon>::const_iterator it = muons->begin(); it != muons->end(); ++it) {
			// exit from loop when you reach the required number of muons
			if (px->size() >= maxSize)
				break;
			if (!( it->isGlobalMuon() || it->isTrackerMuon() ) )
				continue;

			double trkd0 = it->track()->d0();

			if (beamSpotCorr && beamSpot.isValid()) {
				trkd0 = -(it->track()->dxy(beamSpot->position()));
			} else if (beamSpotCorr && !beamSpot.isValid())
				edm::LogError("RootTupleMakerV2_MuonsError") << "Error! Can't get the offlineBeamSpot";

			double minVtxDist3D = 9999.;
			int vtxIndex_ = -1;
//			double vtxDistXY_ = -9999.;
			double vtxDistZ_ = -9999.;

			if (primaryVertices.isValid()) {
				edm::LogInfo("RootTupleMakerV2_MuonsInfo") << "Total # Primary Vertices: " << primaryVertices->size();

				for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin();
						v_it != primaryVertices->end(); ++v_it) {

					double distXY = it->track()->dxy(v_it->position());
					double distZ = it->track()->dz(v_it->position());
					double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

					if (dist3D < minVtxDist3D) {
						minVtxDist3D = dist3D;
						vtxIndex_ = int(std::distance(primaryVertices->begin(), v_it));
//						vtxDistXY_ = distXY;
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
			isPFMuon->push_back(it->isPFMuon());
			numberOfMatches->push_back(it->numberOfMatches());
			numberOfMatchedStations->push_back(it->numberOfMatchedStations());
//			cosmicCompatibility->push_back(it->userFloat("cosmicCompatibility"));
//			timeCompatibility->push_back(it->userFloat("timeCompatibility"));
//			backToBackCompatibility->push_back(it->userFloat("backToBackCompatibility"));
//			overlapCompatibility->push_back(it->userFloat("overlapCompatibility"));
			passID->push_back(it->muonID(muonID));

			//muon isolation variables
			//default
			trkIso03->push_back(it->isolationR03().sumPt);
			ecalIso03->push_back(it->isolationR03().emEt);
			hcalIso03->push_back(it->isolationR03().hadEt);
			hoIso03->push_back(it->isolationR03().hoEt);
			relIso03->push_back(
					(it->isolationR03().sumPt + it->isolationR03().emEt + it->isolationR03().hadEt) / it->pt());
			//bigger cone
			trkIso05->push_back(it->isolationR05().sumPt);
			ecalIso05->push_back(it->isolationR05().emEt);
			hcalIso05->push_back(it->isolationR05().hadEt);
			hoIso05->push_back(it->isolationR05().hoEt);
			relIso05->push_back(
					(it->isolationR05().sumPt + it->isolationR05().emEt + it->isolationR05().hadEt) / it->pt());

			if (storePFIsolation) {
				pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
				pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
				pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);
				pat::IsolationKeys isokeyPfPUChargedHadronIso = pat::IsolationKeys(12);

				double pfRelIso03(0), pfRelIso04(0), pfRelIso05(0);
				double directionalPFIso02(0), directionalPFIso02FallOff(0), pfIso02FallOff(0);
				double directionalPFIso03(0), directionalPFIso03FallOff(0), pfIso03FallOff(0);

				const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
				const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
				const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
				const reco::IsoDeposit * PfPUChargedHadronIso = it->isoDeposit(isokeyPfPUChargedHadronIso);

				directionalPFIso02 = customIsolation(*it, pfCandidates, 0.2, true, false, reco::PFCandidate::e);
				directionalPFIso02FallOff = customIsolation(*it, pfCandidates, 0.2, true, true, reco::PFCandidate::e);
				pfIso02FallOff = customIsolation(*it, pfCandidates, 0.2, false, true, reco::PFCandidate::e);

				directionalPFIso03 = customIsolation(*it, pfCandidates, 0.3, true, false, reco::PFCandidate::e);
				directionalPFIso03FallOff = customIsolation(*it, pfCandidates, 0.3, true, true, reco::PFCandidate::e);
				pfIso03FallOff = customIsolation(*it, pfCandidates, 0.3, false, true, reco::PFCandidate::e);

				DirectionalPFIso02->push_back(directionalPFIso02);
				DirectionalPFIso02FallOff->push_back(directionalPFIso02FallOff);
				PfRelIso02FallOff->push_back(pfIso02FallOff);
				DirectionalPFIso03->push_back(directionalPFIso03);
				DirectionalPFIso03FallOff->push_back(directionalPFIso03FallOff);
				PfRelIso03FallOff->push_back(pfIso03FallOff);

				if (PfChargedHadronIsolation) {
					PfChargedHadronIso03->push_back(PfChargedHadronIsolation->depositWithin(0.3));
					PfChargedHadronIso04->push_back(PfChargedHadronIsolation->depositWithin(0.4));
					PfChargedHadronIso05->push_back(PfChargedHadronIsolation->depositWithin(0.5));
					pfRelIso03 += PfChargedHadronIsolation->depositWithin(0.3);
					pfRelIso04 += PfChargedHadronIsolation->depositWithin(0.4);
					pfRelIso05 += PfChargedHadronIsolation->depositWithin(0.5);
					
					sumChargedHadronPt03->push_back(it->pfIsolationR03().sumChargedHadronPt);
					sumChargedHadronPt04->push_back(it->pfIsolationR04().sumChargedHadronPt);
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfChargedHadronIsolation";
				if (PfNeutralHadronIsolation) {
					PfNeutralHadronIso03->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
					PfNeutralHadronIso04->push_back(PfNeutralHadronIsolation->depositWithin(0.4));
					PfNeutralHadronIso05->push_back(PfNeutralHadronIsolation->depositWithin(0.5));
					pfRelIso03 += PfNeutralHadronIsolation->depositWithin(0.3);
					pfRelIso04 += PfNeutralHadronIsolation->depositWithin(0.4);
					pfRelIso05 += PfNeutralHadronIsolation->depositWithin(0.5);
					
					sumNeutralHadronPt03->push_back(it->pfIsolationR03().sumNeutralHadronEt);
					sumNeutralHadronPt04->push_back(it->pfIsolationR04().sumNeutralHadronEt);
					
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfNeutralHadronIsolation";
				if (PFGammaIsolation) {
					PFGammaIso03->push_back(PFGammaIsolation->depositWithin(0.3));
					PFGammaIso04->push_back(PFGammaIsolation->depositWithin(0.4));
					PFGammaIso05->push_back(PFGammaIsolation->depositWithin(0.5));
					pfRelIso03 += PFGammaIsolation->depositWithin(0.3);
					pfRelIso04 += PFGammaIsolation->depositWithin(0.4);
					pfRelIso05 += PFGammaIsolation->depositWithin(0.5);
					
					sumPhotonPt03->push_back(it->pfIsolationR03().sumPhotonEt);
					sumPhotonPt04->push_back(it->pfIsolationR04().sumPhotonEt);
				} else
					edm::LogError("BristolNTuple_MuonsExtraError") << "Error! Can't get the isolation deposit "
							<< "PFGammaIsolation";
				
				sumPUPt03->push_back(it->pfIsolationR03().sumPUPt);
				sumPUPt04->push_back(it->pfIsolationR04().sumPUPt);
				
				
				PFRelIso03->push_back(pfRelIso03 / it->pt());
				PFRelIso04->push_back(pfRelIso04 / it->pt());
				PFRelIso05->push_back(pfRelIso05 / it->pt());
				PFRelIso03DeltaBeta->push_back(getRelativeIsolation(*it, 0.3, true));
				PFRelIso04DeltaBeta->push_back(getRelativeIsolation(*it, 0.4, true));

				if (PfPUChargedHadronIso) {
					PfPUChargedHadronIso03->push_back(PfPUChargedHadronIso->depositWithin(0.3));
					PfPUChargedHadronIso04->push_back(PfPUChargedHadronIso->depositWithin(0.4));
					PfPUChargedHadronIso05->push_back(PfPUChargedHadronIso->depositWithin(0.5));
				} else
					edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfPUChargedHadronIso";
			}

			//associated track
			trkD0->push_back(trkd0);
			trkD0Error->push_back(it->track()->d0Error());
			trkDz->push_back(it->track()->dz());
			trkDzError->push_back(it->track()->dzError());
			trackValidFractionOfHits->push_back(it->track()->validFraction());

			//associated global track
			if ( !( it->globalTrack().isNull() ) ) {
				globalChi2->push_back(it->globalTrack()->normalizedChi2());
				globalTrackNumberOfValidMuonHits->push_back(it->globalTrack()->hitPattern().numberOfValidMuonHits());
			}
			else {
				globalChi2->push_back(99999);
				globalTrackNumberOfValidMuonHits->push_back(-1);
			}

			//associated inner track
			innerTrackNumberOfValidHits->push_back(it->innerTrack()->numberOfValidHits());
			innerTrackPixelLayersWithMeasurement->push_back(
					it->innerTrack()->hitPattern().pixelLayersWithMeasurement());
			innerTrackTrackerLayersWithMeasurement->push_back(
					it->innerTrack()->hitPattern().trackerLayersWithMeasurement());
			innerTrackNumberOfValidPixelHits->push_back(it->innerTrack()->hitPattern().numberOfValidPixelHits());
			//muon vertex variables
			vtxIndex->push_back(vtxIndex_);
			vtxDistZ->push_back(vtxDistZ_);
			primaryVertexDXY->push_back(it->dB());
			primaryVertexDXYError->push_back(it->edB());
			beamSpotDXY->push_back(it->dB(pat::Muon::BS2D));
			beamSpotDXYError->push_back(it->edB(pat::Muon::BS2D));
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
	iEvent.put(energy, prefix + "Energy" + suffix);

	//extra properties
	iEvent.put(charge, prefix + "Charge" + suffix);

	//muon ID variables
	iEvent.put(isGlobalMuon, prefix + "isGlobalMuon" + suffix);
	iEvent.put(isTrackerMuon, prefix + "isTrackerMuon" + suffix);
	iEvent.put(isPFMuon, prefix + "isPFMuon" + suffix);
	iEvent.put(numberOfMatches, prefix + "NumberOfMatches" + suffix);
	iEvent.put(numberOfMatchedStations, prefix + "NumberOfMatchedStations" + suffix);
	iEvent.put(passID, prefix + "PassID" + suffix);

	//muon isolation variables
	//default
	iEvent.put(trkIso03, prefix + "TrkIso03" + suffix);
	iEvent.put(ecalIso03, prefix + "EcalIso03" + suffix);
	iEvent.put(hcalIso03, prefix + "HcalIso03" + suffix);
	iEvent.put(hoIso03, prefix + "HOIso03" + suffix);
	iEvent.put(relIso03, prefix + "RelIso03" + suffix);
	//bigger cone
	iEvent.put(trkIso05, prefix + "TrkIso05" + suffix);
	iEvent.put(ecalIso05, prefix + "EcalIso05" + suffix);
	iEvent.put(hcalIso05, prefix + "HcalIso05" + suffix);
	iEvent.put(hoIso05, prefix + "HOIso05" + suffix);
	iEvent.put(relIso05, prefix + "RelIso05" + suffix);

	//muon PF isolation variables
	if (storePFIsolation) {
		iEvent.put(PfChargedHadronIso03, prefix + "PfChargedHadronIso03" + suffix);
		iEvent.put(PfNeutralHadronIso03, prefix + "PfNeutralHadronIso03" + suffix);
		iEvent.put(PFGammaIso03, prefix + "PFGammaIso03" + suffix);
		iEvent.put(PFRelIso03, prefix + "PFRelIso03" + suffix);

		iEvent.put(PfChargedHadronIso04, prefix + "PfChargedHadronIso04" + suffix);
		iEvent.put(PfNeutralHadronIso04, prefix + "PfNeutralHadronIso04" + suffix);
		iEvent.put(PFGammaIso04, prefix + "PFGammaIso04" + suffix);
		iEvent.put(PFRelIso04, prefix + "PFRelIso04" + suffix);
		

		iEvent.put(PfChargedHadronIso05, prefix + "PfChargedHadronIso05" + suffix);
		iEvent.put(PfNeutralHadronIso05, prefix + "PfNeutralHadronIso05" + suffix);
		iEvent.put(PFGammaIso05, prefix + "PFGammaIso05" + suffix);
		iEvent.put(PFRelIso05, prefix + "PFRelIso05" + suffix);

		iEvent.put(DirectionalPFIso02, prefix + "DirectionalPFIso02" + suffix);
		iEvent.put(DirectionalPFIso02FallOff, prefix + "DirectionalPFIso02FallOff" + suffix);
		iEvent.put(PfRelIso02FallOff, prefix + "PfRelIso02FallOff" + suffix);
		iEvent.put(DirectionalPFIso03, prefix + "DirectionalPFIso03" + suffix);
		iEvent.put(DirectionalPFIso03FallOff, prefix + "DirectionalPFIso03FallOff" + suffix);
		iEvent.put(PfRelIso03FallOff, prefix + "PfRelIso03FallOff" + suffix);

		iEvent.put(PfPUChargedHadronIso03, prefix + "PfPUChargedHadronIso03" + suffix);
		iEvent.put(PfPUChargedHadronIso04, prefix + "PfPUChargedHadronIso04" + suffix);
		iEvent.put(PfPUChargedHadronIso05, prefix + "PfPUChargedHadronIso05" + suffix);
		
		//new iso vars
		iEvent.put(sumChargedHadronPt03, prefix + "sumChargedHadronPt03" + suffix);
		iEvent.put(sumChargedHadronPt04, prefix + "sumChargedHadronPt04" + suffix);
		iEvent.put(sumNeutralHadronPt03, prefix + "sumNeutralHadronPt03" + suffix);
		iEvent.put(sumNeutralHadronPt04, prefix + "sumNeutralHadronPt04" + suffix);
		iEvent.put(sumPhotonPt03, prefix + "sumPhotonPt03" + suffix);
		iEvent.put(sumPhotonPt04, prefix + "sumPhotonPt04" + suffix);
		iEvent.put(sumPUPt03, prefix + "sumPUPt03" + suffix);
		iEvent.put(sumPUPt04, prefix + "sumPUPt04" + suffix);
		
		iEvent.put(PFRelIso03DeltaBeta, prefix + "PFRelIso03DeltaBeta" + suffix);
		iEvent.put(PFRelIso04DeltaBeta, prefix + "PFRelIso04DeltaBeta" + suffix);
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
	iEvent.put(innerTrackTrackerLayersWithMeasurement, prefix + "InnerTrack.TrackerLayersWithMeasurement" + suffix);
	iEvent.put(innerTrackNumberOfValidPixelHits, prefix + "InnerTrack.NumberOfValidPixelHits" + suffix);

	//muon vertex variables
	iEvent.put(vtxIndex, prefix + "Vertex.Index" + suffix);
	iEvent.put(vtxDistZ, prefix + "Vertex.DistZ" + suffix);

	iEvent.put(primaryVertexDXY, prefix + "PrimaryVertexDXY" + suffix);
	iEvent.put(primaryVertexDXYError, prefix + "PrimaryVertexDXYError" + suffix);
	iEvent.put(beamSpotDXY, prefix + "BeamSpotDXY" + suffix);
	iEvent.put(beamSpotDXYError, prefix + "BeamSpotDXYError" + suffix);
}
