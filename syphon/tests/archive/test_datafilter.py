"""syphon.tests.archive.test_datafilter.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
import random
from os import environ

import pytest
from pandas import concat, DataFrame, Series
from pandas.testing import assert_frame_equal
from pandas.util.testing import makeCustomIndex
from sortedcontainers import SortedDict
from syphon.archive import datafilter

from .. import make_dataframe

MAX_ROWS = 10
MAX_COLS = 5

class TestDataFilter(object):
    random.seed(a=751)#int(environ['PYTHONHASHSEED']))

    def _build_dataframes(self, frame: DataFrame,
                          meta_cvals: dict,
                          keylist: list,
                          result=[]) -> list:
        this_keylist = keylist.copy()
        this_keylist.reverse()
        header = None
        try:
            header = this_keylist.pop()
        except IndexError:
            result.append(frame)
            return result
        except:
            raise

        for val in meta_cvals[header]:
            rows, _ = frame.shape
            new_col = Series([val]*rows, name=header)
            this_frame = concat([frame.copy(), new_col], axis=1)
            try:
                result = self._build_dataframes(this_frame, meta_cvals,
                                                this_keylist, result=result)
            except:
                raise
        return result

    @pytest.mark.slow
    @pytest.mark.parametrize('rows', [r for r in range(1, MAX_ROWS + 1)])
    @pytest.mark.parametrize('cols', [c for c in range(1, MAX_COLS + 1)])
    def test_datafilter(self, rows, cols, metadata_columns):
        data = make_dataframe(rows, cols)
        meta_col_vals = metadata_columns.copy()
        keys = list(metadata_columns.keys())

        expected = self._build_dataframes(data, meta_col_vals, keys)

        schema = SortedDict()
        index = 0
        for k in keys:
            schema[str(index)] = k
            index += 1

        alldata = DataFrame()
        for f in expected:
            alldata = concat([alldata, f])
        alldata.reset_index(drop=True, inplace=True)

        actual = datafilter(schema, alldata)

        for e in expected:
            match = None
            for a in actual:
                if e.equals(a):
                    match = a.copy()
                    break
            if match is not None:
                assert_frame_equal(e, match)
            else:
                msg='Could not find a matching frame in the filtered list.'
                pytest.fail(msg=msg)
