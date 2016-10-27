#!/bin/bash
unset PYTHONPATH
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

TOPQ_CONDA_PATH=/software/TopQuarkGroup/miniconda; export TOPQ_CONDA_PATH
if [ ! -d "${TOPQ_CONDA_PATH}" ] ; then
  # just create all parent folders except miniconda
  echo "Could not find conda install in ${TOPQ_CONDA_PATH}. Installing conda ..."
  mkdir -p ${TOPQ_CONDA_PATH}; rmdir ${TOPQ_CONDA_PATH}
  wget -nv https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh
  bash miniconda.sh -b -p ${TOPQ_CONDA_PATH}
  PATH=${TOPQ_CONDA_PATH}/bin:$PATH; export PATH
  rm -f miniconda.sh
  echo "Finished conda installation, creating new conda environment"
  conda update conda -y
  conda update pip -y
  conda install psutil -y
  conda config --add channels http://conda.anaconda.org/NLeSC
  conda config --set show_channel_urls yes
  # python modules
  conda create -n ntp python=2.7 root=6 root-numpy numpy matplotlib nose \
  sphinx pytables rootpy pandas -y
  echo "Created conda environment, installing basic dependencies"
  source activate ntp
  conda install git wget pycurl -y
  pip install -U -r requirements.txt
  # clean the cache (downloaded tarballs)
  conda clean -t -y
  # give the group write access
  chmod g+r -R ${TOPQ_CONDA_PATH}
else
  echo "Found conda install in ${TOPQ_CONDA_PATH}, activating..."
  PATH=${TOPQ_CONDA_PATH}/bin:$PATH; export PATH
  source activate ntp
fi

if [ -n "${HEP_PROJECT_ROOT}" ] ; then
   old_projectbase=${HEP_PROJECT_ROOT}
fi


if [ "x${BASH_ARGV[0]}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/project/is" before calling ". bin/env.sh" for this version of bash!
        HEP_PROJECT_ROOT=; export HEP_PROJECT_ROOT
        return 1
    fi
    HEP_PROJECT_ROOT="$PWD"; export HEP_PROJECT_ROOT
else
    # get param to "."
    envscript=$(dirname ${BASH_ARGV[0]})
    HEP_PROJECT_ROOT=$(cd ${envscript}/..;pwd); export HEP_PROJECT_ROOT
fi

if [ -n "${old_projectbase}" ] ; then
   if [ -n "${PATH}" ]; then
      drop_from_path "$PATH" ${old_projectbase}/bin
      drop_from_path "$PATH" ${old_projectbase}/external/miniconda/bin
      PATH=$newpath
   fi
   if [ -n "${PYTHONPATH}" ]; then
      drop_from_path $PYTHONPATH ${old_projectbase}/python
      PYTHONPATH=$newpath
   fi
fi

if [ -z "${PATH}" ]; then
   PATH=$HEP_PROJECT_ROOT/bin; export PATH
else
   PATH=$HEP_PROJECT_ROOT/bin:$PATH; export PATH
fi

if [ -z "${PYTHONPATH}" ]; then
   PYTHONPATH=$HEP_PROJECT_ROOT/python; export PYTHONPATH
else
   PYTHONPATH=$HEP_PROJECT_ROOT/python:$PYTHONPATH; export PYTHONPATH
fi

unset old_projectbase
unset envscript

# for CMSSW
if [ -f /cvmfs/cms.cern.ch/cmsset_default.sh ]; then
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git
fi

# CRAB submission
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Releases#Improvements_enhancements_change
if [ -f /cvmfs/cms.cern.ch/crab3/crab.sh ]; then
	source /cvmfs/cms.cern.ch/crab3/crab.sh
fi

# for grid tools
vomsInfo=`which voms-proxy-info &> /dev/null`
if [ "$vomsInfo" == "" ]; then
  if [ -f /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh ]; then
	source /cvmfs/grid.cern.ch/etc/profile.d/setup-cvmfs-ui.sh
	# the UI uses an old java version, we do not want that
	unset JAVA_HOME
  else
    echo "Cannot find voms-proxy-info nor setup-cvmfs-ui.sh"
  fi
fi

if [ ! -d "DEV" ] ; then
  mkdir DEV
fi

echo "NTP is now available in $PWD"

if [ ! -d ${HEP_PROJECT_ROOT}/external ] ; then
  mkdir ${HEP_PROJECT_ROOT}/external
  pip install -U --install-option="--prefix=${HEP_PROJECT_ROOT}/external" git+https://github.com/BristolTopGroup/DailyPythonScripts.git
fi

# adjusting paths for dps
PATH=${HEP_PROJECT_ROOT}/external/bin:$PATH; export PATH
PYTHONPATH=${HEP_PROJECT_ROOT}/external/lib/python2.7/site-packages:$PYTHONPATH; export PYTHONPATH
if [ ! -e "DEV/DPS" ]; then
  ln -s ../external/lib/python2.7/site-packages/dps DEV/DPS
fi
echo "DPS is now available in DEV/DPS"
