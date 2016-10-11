"""
    get ttjet normalisation:
        Runs DailyPythonScripts/dps/analysis/xsection/01_get_ttjet_normalisation.py
        
    Usage:
        get ttjet normalisation [--centre_of_mass_energy <centre of mass energy>]\
                                [--variable <variable>] \
                                [--closure_test_type <type>] \
                                [--test] [--closure_test] [--visiblePS]
        
    Flags:
        closure_test:
            Perform fit on data == sum(MC) * scale factor (MC process)

        test:
            Just run the central measurement

        visiblePS:
            Unfold to visible phase space (instead of full phase space)
    
    Parameters: 
        centre_of_mass_energy: 
            set the centre of mass energy for analysis. Default = 13 [TeV]

        variable:
            set the variable to analyse ({variables}). Default is MET.

        closure_test_type:
            Type of closure test (relative normalisation): {closure_tests}
"""
import logging
import glob
import os

from hepshell.interpreter import time_function

from ntp.commands.run import Command as C
from ntp.commands.setup import DPS_RESULTDIR
from ntp.commands.create.dps.configs import DPS_CONFIGDIR

from dps.analysis.xsection.lib import closure_tests as CTs
from dps.config.xsection import XSectionConfig

LOG = logging.getLogger(__name__)
INPUT_PATH = os.path.join(
    DPS_CONFIGDIR, 'measurements', 'background_subtraction')


class Command(C):
    REQUIRE_GRID_CERT = False

    DEFAULTS = {
        'centre_of_mass_energy': 13,
        'variable': 'MET',
        'closure_test_type': 'simple',
        'output_path': DPS_RESULTDIR,
        'input_path': INPUT_PATH,
        'closure_test': False,
        'visiblePS': False,
        'test': False,
    }

    def __init__(self, path=__file__, doc=__doc__):
        variables = '|'.join(XSectionConfig.variables)
        closure_tests = '|'.join(CTs.keys())
        doc = doc.format(variables=variables, closure_tests=closure_tests)
        super(Command, self).__init__(path, doc)

    @time_function('get ttjet normalisation', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__run()
        return True

    def __run(self):
        import importlib
        get_ttjet_normalisation = importlib.import_module(
            'dps.analysis.xsection.01_get_ttjet_normalisation', 'dps.analysis.xsection')

        measurement_config = XSectionConfig(
            self.__variables['centre_of_mass_energy'])
        # caching of variables for shorter access
        variable = self.__variables['variable']
        closure_test_type = self.__variables['closure_test_type']

        output_path = self.__variables['output_path']
        if self.__variables['closure_test']:
            output_path = os.path.join(
                output_path, 'closure_test', closure_test_type)

        # construct categories from files:
        input_template = os.path.join(
            INPUT_PATH, '{energy}TeV', '{channel}', '{variable}', '{phase_space}', '*.json'
        )
        categories = ['QCD_shape']
        categories.extend(measurement_config.categories_and_prefixes.keys())
        categories.extend(measurement_config.rate_changing_systematics_names)
        categories.extend([measurement_config.vjets_theory_systematic_prefix +
                           systematic for systematic in measurement_config.generator_systematics])

        phase_space = 'FullPS'
        if self.__variables['visiblePS']:
            phase_space = 'VisiblePS'
        results = {}
        for channel in ['electron', 'muon']:
            inputs = {
                'energy': self.__variables['centre_of_mass_energy'],
                'channel': channel,
                'variable': variable,
                'phase_space': phase_space,
            }
            measurement_files = glob.glob(input_template.format(**inputs))
            Measurement = get_ttjet_normalisation.Measurement
            TTJetNormalisation = get_ttjet_normalisation.TTJetNormalisation
            for f in sorted(measurement_files):
                if self.__variables['test'] and not f.endswith('central.json'):
                    continue
                LOG.info('Processing file {0}'.format(f))
                measurement = Measurement.fromJSON(f)
                # for each measurement
                norm = TTJetNormalisation(
                    config=measurement_config,
                    measurement=measurement,
                    method=TTJetNormalisation.BACKGROUND_SUBTRACTION,
                    phase_space=phase_space,
                )
                norm.calculate_normalisation()
                LOG.info('Saving results to {0}'.format(output_path))
                norm.save(output_path)
                # store results for later combination
                r_name = f.replace(channel, '')
                if not results.has_key(r_name):
                    results[r_name] = [norm]
                else:
                    results[r_name].append(norm)

        for f, r_list in results.items():
            if not len(r_list) == 2:
                msg = 'Only found results ({0}) for one channel, not combining.'
                LOG.warn(msg.format(f))
                continue
            n1, n2 = r_list
            n1.combine(n2)
            n1.save(output_path)
