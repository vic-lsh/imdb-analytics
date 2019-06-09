import yaml

CONFIG_FNAME = "config.yml"


class AnalyzerConfig:

    class TVSeriesUndefinedException(Exception):
        pass

    def __init__(self, fname=CONFIG_FNAME):
        with open(fname, 'r') as cfgfile:
            cfg = yaml.safe_load(cfgfile)
        if 'tv_series' not in cfg:
            self.__tv_series_names = []
            raise TVSeriesUndefinedException
        else:
            self.__tv_series_names = cfg['tv_series']
        if 'headless' in cfg:
            self.__headless = cfg['headless']
        else:
            self.__headless = True

    @property
    def tv_series_names(self):
        return self.__tv_series_names

    @property
    def headless(self):
        return self.__headless
