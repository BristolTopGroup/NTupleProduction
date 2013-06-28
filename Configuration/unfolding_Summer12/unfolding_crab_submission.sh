#!/bin/bash
#better not to run the script but copy and paste commands in packs of ~8 (on soolin)
#creating the jobs
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_Summer12_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola_Summer12_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola_Summer12_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola_Summer12_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola_Summer12_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding.cfg &
nohup crab -create -cfg BristolAnalysis/NTupleTools/Configuration/unfolding_Summer12/TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding.cfg &

#submitting in packs of 500 (remoteGlideIn constraint)
nohup crab -submit 1-500 -c TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_unfolding/ &
nohup crab -submit 1-500 -c TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1-500 -c TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1-500 -c TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1-500 -c TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &

nohup crab -submit 1-500 -c TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1-500 -c TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding/ &
nohup crab -submit 501-1000 -c TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 501-1000 -c TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding/ &
nohup crab -submit 1001-1500 -c TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1001-1500 -c TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding/ &
nohup crab -submit 1501-2000 -c TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit 1501-2000 -c TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding/ &

#this is to top up the jobs - needs to be run after most of the jobs are submitted
nohup crab -submit -c TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_unfolding/ &
nohup crab -submit -c TT_8TeV-mcatnlo_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit -c TT_CT10_TuneZ2star_8TeV-powheg-tauola_Summer12_DR53X-PU_S10_START53_V7A-v2_unfolding/ &

nohup crab -submit -c TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit -c TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit -c TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
nohup crab -submit -c TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_unfolding/ &
