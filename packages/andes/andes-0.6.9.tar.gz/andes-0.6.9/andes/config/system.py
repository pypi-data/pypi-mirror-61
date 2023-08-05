import importlib
import logging

from . import ConfigBase
from ..utils.cached import cached

logger = logging.getLogger(__name__)
try:
    klu = importlib.import_module('cvxoptklu.klu')
except ImportError:
    klu = None


class System(ConfigBase):
    def __init__(self, **kwargs):
        self.freq = 60.0
        self.mva = 100.0
        self.distrsw = False
        self.sparselib = 'klu'
        self.sparselib_alt = ['klu', 'umfpack', 'spsolve', 'cupy']
        self.export = 'txt'
        self.export_alt = ['txt', 'latex']
        self.coi = False
        self.connectivity = False
        self.error = 1
        self.static = 0
        self.nseries = 0
        self.forcepq = False
        self.forcez = False
        self.base = True
        self.dime_enable = False
        self.dime_name = 'sim'
        self.dime_server = 'ipc:///tmp/dime'
        super(System, self).__init__(**kwargs)

    @cached
    def config_descr(self):
        descriptions = {
            'freq': 'system base frequency',
            'mva': 'system base MVA',
            'distrsw': 'use distributed slack bus mode',
            'sparselib': 'sparse matrix library name',
            'export': 'help documentation export format',
            'coi': 'using Center of Inertia',
            'connectivity': 'connectivity check during TDS',
            'forcepq': 'force to use constant PQ load',
            'forcez': 'force to convert load to impedance',
            'base': 'convert  parameters to the system base',
        }
        return descriptions

    def check(self):
        """
        Check config data consistency

        Returns
        -------

        """
        if self.sparselib not in self.sparselib_alt:
            logger.warning("Invalid sparse library <{}>".format(self.sparselib))
            self.sparselib = 'umfpack'

        if self.sparselib == 'klu' and (klu is None):
            logger.info("KLU not found. Install with \"pip install cvxoptklu\" ")
            self.sparselib = 'umfpack'

        elif self.sparselib == 'cupy':
            try:
                cupy_sparse = importlib.import_module('cupyx.scipy.sparse')
                cupy_solve = importlib.import_module('cupyx.scipy.sparse.linalg.solve')
                _ = getattr(cupy_sparse, 'csc_matrix')  # NOQA
                _ = getattr(cupy_solve, 'lsqr')  # NOQA
            except (ImportError, AttributeError):
                logger.info("CuPy not found. Fall back to UMFPACK.")
                self.sparselib = 'umfpack'

        return True
