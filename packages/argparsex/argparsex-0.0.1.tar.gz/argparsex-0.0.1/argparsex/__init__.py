import argparse

SUPPRESS = argparse.SUPPRESS

class SentinelValue:
    pass

class ArgumentParser(argparse.ArgumentParser):
    _supplied_defaults = None
    _defaults = None

    def parse_supplied_args(self, args=None, namespace=None):
        sentinel = SentinelValue()
        real_defaults = {}
        dict_ = self.__dict__['_option_string_actions']
        for key, val in dict_.items():
            if val.default != SUPPRESS and val.default != sentinel:
                real_defaults[val.dest] = val.default
                val.default = sentinel

        supplied_vals = {}
        supplied_default_vals = {}
        default_vals = {}

        for key, val in vars(super().parse_args(args, namespace)).items():
            if val != sentinel:
                if key not in real_defaults or val != real_defaults[key]:
                    supplied_vals[key] = val
                else:
                    supplied_default_vals[key] = val
            else:
                default_vals[key] = real_defaults[key]

        self._supplied_defaults = argparse.Namespace(**supplied_default_vals)
        self._defaults = argparse.Namespace(**default_vals)

        return argparse.Namespace(**supplied_vals)

    def parse_supplied_default_args(self, args=None, namespace=None):
        if self._supplied_defaults is None:
            self.parse_args(args, namespace)

        return self._supplied_defaults

    def parse_default_args(self, args=None, namespace=None):
        if self._defaults is None:
            self.parse_args(args, namespace)

        return self._defaults
