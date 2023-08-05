from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from andes import main  # NOQA
from andes import filters  # NOQA
from andes.main import run, run_stock  # NOQA


__author__ = 'Hantao Cui'

__all__ = ['main', 'consts', 'plot', 'system',
           'config', 'filters', 'models', 'routines', 'utils', 'variables']
