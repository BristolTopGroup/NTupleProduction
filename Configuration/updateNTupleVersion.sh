OLDVERSION=8c
NEWVERSION=9a

#change parameters
#OLDVERSION='use44X=1'
#NEWVERSION='CMSSW=44X'

folders=( data2011  data2012  defaultMC_Fall11  defaultMC_Summer12  differentTOPmasses_Fall11  systematicSamples_Fall11  systematicSamples_Summer12  zprime_Fall11  zprime_Summer12)
for folder in "${folders[@]}"
do
	sed -i "s/${OLDVERSION}/${NEWVERSION}/g" $folder/*.*
done