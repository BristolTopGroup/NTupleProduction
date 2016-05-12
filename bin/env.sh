#!/bin/bash
drop_from_path()
{
   # Assert that we got enough arguments
   if test $# -ne 2 ; then
      echo "drop_from_path: needs 2 arguments"
      return 1
   fi

   p=$1
   drop=$2

   newpath=`echo $p | sed -e "s;:${drop}:;:;g" \
                          -e "s;:${drop};;g"   \
                          -e "s;${drop}:;;g"   \
                          -e "s;${drop};;g"`
}


if [ -n "${NTPROOT}" ] ; then
   old_ntpbase=${NTPROOT}
fi


if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/NTupleProdcution/is" before calling ". bin/env.sh" for this version of bash!
        NTPROOT=; export NTPROOT
        return 1
    fi
    NTPROOT="$PWD"; export NTPROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    NTPROOT=$(cd ${envscript}/..;pwd); export NTPROOT
fi

if [ -n "${old_ntpbase}" ] ; then
   if [ -n "${PATH}" ]; then
      drop_from_path "$PATH" ${old_ntpbase}/bin
      PATH=$newpath
   fi
   if [ -n "${PYTHONPATH}" ]; then
      drop_from_path $PYTHONPATH ${old_ntpbase}/python
      PYTHONPATH=$newpath
   fi
fi


if [ -z "${PATH}" ]; then
   PATH=$NTPROOT/bin; export PATH
else
   PATH=$NTPROOT/bin:$PATH; export PATH
fi

if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=$NTPROOT/python; export PYTHONPATH
else
   PYTHONPATH=$NTPROOT/python:$PYTHONPATH; export PYTHONPATH
fi

# for CMSSW
source /cvmfs/cms.cern.ch/cmsset_default.sh
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git

# CRAB submission
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Releases#Improvements_enhancements_change
source /cvmfs/cms.cern.ch/crab3/crab_light.sh

# for grid tools
source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh

unset old_ntpbase
unset envscript
