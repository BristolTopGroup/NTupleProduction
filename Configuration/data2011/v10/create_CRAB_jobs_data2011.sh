#crab -create -cfg BristolAnalysis/NTupleTools/Configuration/data2011/v10/ElectronHad-Run2011A-08Nov2011-v1_LeptonPlus3JetsSkim.cfg
#for i in `seq 1 10`;
#do
#crab -submit 500 -c ElectronHad_Run2011A-08Nov2011-v1_GoldenJSON_nTuple_v10_LeptonPlus3Jets_Dec2013
#done

#crab -create -cfg BristolAnalysis/NTupleTools/Configuration/data2011/v10/ElectronHad-Run2011B-19Nov2011-v1_LeptonPlus3JetsSkim.cfg &> eleHad2011B.log
#for i in `seq 1 10`;
#do
#crab -submit 500 -c ElectronHad_Run2011B-19Nov2011-v1_GoldenJSON_nTuple_v10_LeptonPlus3Jets_Dec2013
#done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/data2011/v10/SingleMu-Run2011A-08Nov2011-v1_LeptonPlus3JetsSkim.cfg &> singleMu2011A.log
for i in `seq 1 10`;
do
crab -submit 500 -c SingleMu_Run2011A-08Nov2011-v1_GoldenJSON_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/data2011/v10/SingleMu-Run2011B-19Nov2011-v1_LeptonPlus3JetsSkim.cfg &> singleMu2011B.log
for i in `seq 1 10`;
do
crab -submit 500 -c SingleMu_Run2011B-19Nov2011-v1_GoldenJSON_nTuple_v10_LeptonPlus3Jets_Dec2013
done