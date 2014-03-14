#run with: nohup ./BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/create_CRAB_jobs_systematicSamples_Fall11.sh

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TT_noCorr_7TeV-mcatnlo_Fall11_LeptonPlus3JetsSkim.cfg
for i in `seq 1 10`;
do
crab -submit 500 -c TT_noCorr_7TeV-mcatnlo_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TT_TuneZ2_7TeV-mcatnlo_Fall11_LeptonPlus3JetsSkim.cfg &> tt_mcatnlo.log
for i in `seq 1 10`;
do
crab -submit 500 -c TT_TuneZ2_7TeV-mcatnlo_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TT_TuneZ2_7TeV-powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_poweg.log
for i in `seq 1 10`;
do
crab -submit 500 -c TT_TuneZ2_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TT_TuneZ2_7TeV-pythia6-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_pythia.log
for i in `seq 1 10`;
do
crab -submit 500 -c TT_TuneZ2_7TeV-pythia6-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TTJets_TuneP11noCR_7TeV-madgraph-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_noCR.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTJets_TuneP11noCR_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TTjets_TuneZ2_matchingdown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_matchingdown.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v3_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TTjets_TuneZ2_matchingup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_matchingup.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TTjets_TuneZ2_scaledown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_scaledown.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v3_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/TTjets_TuneZ2_scaleup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> tt_scaleup.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v3_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/WJetsToLNu_TuneZ2_matchingdown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> wjets_matchingdown.log
for i in `seq 1 10`;
do
crab -submit 500 -c WJetsToLNu_TuneZ2_matchingdown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/WJetsToLNu_TuneZ2_matchingup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> wjets_matchingup.log
for i in `seq 1 10`;
do
crab -submit 500 -c WJetsToLNu_TuneZ2_matchingup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/WJetsToLNu_TuneZ2_scaledown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> wjets_scaledown.log
for i in `seq 1 10`;
do
crab -submit 500 -c WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/WJetsToLNu_TuneZ2_scaleup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> wjets_scaleup.log
for i in `seq 1 10`;
do
crab -submit 500 -c WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/ZJetsToLL_TuneZ2_matchingdown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> zjets_matchingdown.log
for i in `seq 1 10`;
do
crab -submit 500 -c ZJetsToLL_TuneZ2_matchingdown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/ZJetsToLL_TuneZ2_matchingup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> zjets_matchingup.log
for i in `seq 1 10`;
do
crab -submit 500 -c ZJetsToLL_TuneZ2_matchingup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/ZJetsToLL_TuneZ2_scaledown_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> zjets_scaledown.log
for i in `seq 1 10`;
do
crab -submit 500 -c ZJetsToLL_TuneZ2_scaledown_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/systematicSamples_Fall11/v10/ZJetsToLL_TuneZ2_scaleup_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> zjets_scaleup.log
for i in `seq 1 10`;
do
crab -submit 500 -c ZJetsToLL_TuneZ2_scaleup_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done