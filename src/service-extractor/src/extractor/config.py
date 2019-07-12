import os
import yaml

CONFIG_FNAME = "cfg/base_cfg.yml"


class ExtractorConfig:
    """This class contains configurations specified in the config file.
    The default location for config file is `src/config.yml`.
    """

    def __init__(self, fname=CONFIG_FNAME):
        try:
            assert os.path.isfile(fname)
            with open(os.path.abspath(fname), 'r') as cfgfile:
                cfg = yaml.safe_load(cfgfile)
        except AssertionError:
            print("Error: \tNo config file. Exiting...")
            exit(1)

        self.__tv_series_names = []
        self.__headless = True
        self.__serialization = True
        self.__serialization_fname = "src/pickle"

        if 'tv_series' not in cfg:
            self.__tv_series_names = []
        else:
            self.__tv_series_names = cfg['tv_series']

        if 'headless' in cfg:
            self.__headless = cfg['headless']

        if 'pickle' in cfg:
            if 'should_pickle' in cfg['pickle']:
                self.__serialization = cfg['pickle']['should_pickle']
            if 'pickle_filename' in cfg['pickle']:
                self.__serialization_fname = cfg['pickle']['pickle_filename']

    @property
    def should_serialize(self) -> bool:
        """Returns if serialization is on or off, default to on if not
        specified in config."""
        return self.__serialization

    @property
    def serialization_filename(self) -> str:
        """Returns the filename used for serialization, default to None if
        serialization is off."""
        if not self.__serialization:
            return None
        else:
            return self.__serialization_fname

    @property
    def tv_series_names(self):
        return self.__tv_series_names

    @property
    def headless(self):
        return self.__headless
