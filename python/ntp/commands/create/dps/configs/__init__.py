"""
    create dps configs:
        Runs DailyPythonScripts/dps/analysis/xsection/create_measurement.py
        
    Usage:
        create dps configs [-c]
        
    Parameters:
        --centre-of-mass-energy: 
                set the centre of mass energy for analysis. Default = 13 [TeV]
"""
import logging
import os
from hepshell.interpreter import time_function
from ntp.commands.run import Command as C
from ntp.commands.setup import DPS_RESULTDIR

LOG = logging.getLogger(__name__)
DPS_CONFIGDIR = os.path.join(DPS_RESULTDIR, 'config')


class Command(C):
    REQUIRE_GRID_CERT = False

    DEFAULTS = {
        'centre-of-mass-energy': 13,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('create dps configs', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
#         from dps.analysis.xsection import create_measurement
        # this creates config folder in current directory
#         create_measurement.main()
        self.__create_measurement_main()
        configs = os.path.join(os.getcwd(), 'config')
        # fix output directory
        import shutil
        # rectify move behaviour
        if os.path.exists(DPS_CONFIGDIR):
            shutil.rmtree(DPS_RESULTDIR)
        shutil.move(configs, DPS_CONFIGDIR)

        return True

    def __create_measurement_main(self):
        centre_of_mass_energy = self.__variables['centre-of-mass-energy']
        # set global variables
        from dps.config.xsection import XSectionConfig
        measurement_config = XSectionConfig(centre_of_mass_energy)
        categories = ['QCD_shape']
        categories.extend(measurement_config.categories_and_prefixes.keys())
        categories.extend(measurement_config.rate_changing_systematics_names)
        categories.extend([measurement_config.vjets_theory_systematic_prefix +
                           systematic for systematic in measurement_config.generator_systematics if not ('mass' in systematic or 'hadronisation' in systematic or 'NLO' in systematic)])

        from dps.analysis.xsection.create_measurement import create_measurement
        for variable in measurement_config.variables:
            for category in categories:
                for channel in ['electron', 'muon']:
                    if channel == 'electron' and (category == 'Muon_down' or category == 'Muon_up'):
                        continue
                    elif channel == 'muon' and (category == 'Electron_down' or category == 'Electron_up'):
                        continue
                    create_measurement(
                        centre_of_mass_energy, category, variable, channel,
                        phase_space='FullPS', norm_method='background_subtraction')
                    # and the visible phase space
                    create_measurement(
                        centre_of_mass_energy, category, variable, channel,
                        phase_space='VisiblePS', norm_method='background_subtraction')
