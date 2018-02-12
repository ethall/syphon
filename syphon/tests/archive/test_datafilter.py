"""syphon.tests.archive.test_datafilter.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
import random
from os import environ

import pytest
from pandas import concat, DataFrame, Series
from pandas.util.testing import makeCustomIndex
from syphon.archive import datafilter

from .. import make_dataframe

class TestDataFilter(object):
    random.seed(a=int(environ['PYTHONHASHSEED']))

    max_rows = 10
    max_columns = 5

    @pytest.mark.slow
    @pytest.mark.parametrize(
        'rows',
        [r for r in range(1, TestDataFilter.max_rows + 1)]
    )
    @pytest.mark.parametrize(
        'cols',
        [c for c in range(1, TestDataFilter.max_columns + 1)]
    )
    def test_datafilter(self, rows, cols, metadata_columns):
        expected = []
        frame = make_dataframe(rows, cols)
        for header in metadata_columns:
            column_values = metadata_columns[header]
            for value in column_values:
                frame = concat([
                    frame,
                    Series([value]*rows, name=header)
                ], axis=1)
        ## create list of frames
        ## make schema from meta_headers
        ## concat list of frames into a single DataFrame
        ## send schema and single DataFrame to `datafilter`
        ## for each returned DataFrame, try to match it to one from the list
