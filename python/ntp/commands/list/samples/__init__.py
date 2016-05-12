"""
    samples:    lists all available samples

        Usage:
            list samples [campaign=<X>] [format=<X>]
        Parameters:
            campaign: Filter output by campaign
            format: Choose the display format (table|dict)
                    Default: table
"""
from .. import Command as C
from crab.datasets import create_sample_list, datasets_to_str


def get_text_lenghts(samples):
    campaigns = samples.keys()
    aliases = []
    datasets = []

    for campaign, sample in samples.items():
        aliases.extend(sample.keys())
        datasets.extend(samples.values())

    len_campaigns = [len(c) for c in campaign]
    len_aliases = [len(a) for a in aliases]
    len_datasets = [len(d) for d in datasets]

    return max(len_campaigns), max(len_aliases), max(len_datasets)


class Command(C):

    DEFAULTS = {
        'format': 'table',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        samples = create_sample_list()

        format = self.__variables['format']
        if format == 'dict':
            self.__text = datasets_to_str(samples)
            if 'campaign' in self.__variables:
                restrict_c = self.__variables['campaign']
                self.__text = datasets_to_str(samples[restrict_c])
        else:
            self.__create_table(samples)

        return True

    def __create_table(self, samples):
        headers = ['CAMPAIGN', 'ALIAS', 'DATASET']
        # get maximum lenghts of our columns
        max_len_c, max_len_a, max_len_d = get_text_lenghts(samples)
        # add some space
        max_len_c = max([max_len_c, len(headers[0])])

        row_format = "{:<" + str(max_len_c) + "}\t"
        row_format += "{:<" + str(max_len_a) + "}\t"
        row_format += "{:<" + str(max_len_d) + "}\n"

        self.__text = row_format.format(*headers)
        self.__text += '-' * (max_len_c + max_len_a + max_len_d)
        self.__text += '\n'

        restrict_c = ''
        if 'campaign' in self.__variables:
            restrict_c = self.__variables['campaign']
            if not restrict_c in samples:
                self.__text = 'Campaign "{0}" does not exist.\n'.format(
                    restrict_c)
                self.__text += 'Available campaigns:\n'
                for c in samples.keys():
                    self.__text += '\t{0}\n'.format(c)
        for campaign, sample in samples.items():
            if restrict_c:
                if not campaign == restrict_c:
                    continue
            for alias, dataset in sample.items():
                self.__text += row_format.format(*[campaign, alias, dataset])
            self.__text += '\n'
