'''
Module containing PathSplitter class
'''
# pylint: disable=line-too-long, import-error, too-few-public-methods

from dmu.logging.log_store  import LogStore
from rx_data import utilities as ut

log   = LogStore.add_logger('rx_data:path_splitter')
# ------------------------------------------
class PathSplitter:
    '''
    Class meant to split lists of LFNs/paths/PFNs of ROOT files into
    Samples and HLT2 trigger categories
    '''
    # ------------------------------------------
    def __init__(self, paths : list[str], max_files : int = -1):
        '''
        paths: List of LFNs/PFNs/Local paths
        max_files: If doing tests, the output lists will be limited to this number, default not truncate
        '''
        self._l_path    = paths
        self._max_files = max_files
    # ------------------------------------------
    def _truncate_paths(self, d_path):
        '''
        Will limit the number of paths in the values if Data.Max is larger than zero
        '''

        if self._max_files < 0:
            return d_path

        log.warning(f'Truncating to {self._max_files} paths')

        d_path_trunc = { key : val[:self._max_files] for key, val in d_path.items() }

        return d_path_trunc
    # ------------------------------------------
    def split(self) -> dict[tuple[str,str],list[str]]:
        '''
        Takes list of paths to ROOT files
        Splits them into categories and returns a dictionary:

        category : [path_1, path_2, ...]
        '''
        npath = len(self._l_path)
        log.info(f'Splitting {npath} paths into categories')

        d_info_path = {}
        for path in self._l_path:
            info = ut.info_from_path(path)
            if info not in d_info_path:
                d_info_path[info] = []

            d_info_path[info].append(path)

        d_info_path = self._truncate_paths(d_info_path)

        log.info('Found samples:')
        d_info_path = dict(sorted(d_info_path.items()))
        for sample, line in sorted(d_info_path):
            log.debug(f'{sample:<50}{line:<30}')

        return d_info_path
# ------------------------------------------