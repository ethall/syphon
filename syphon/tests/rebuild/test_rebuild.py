"""syphon.tests.rebuild.test_rebuild.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
import os

import pytest
from pandas import DataFrame, read_csv
from pandas.testing import assert_frame_equal
from sortedcontainers import SortedDict
from syphon import Context
from syphon.archive import archive
from syphon.init import init
from syphon.rebuild import rebuild

from .. import get_data_path

class TestRebuild(object):
    @staticmethod
    def _delete_cache(file: str):
        try:
            os.remove(file)
        except:
            raise

    def test_rebuild_iris(self, archive_dir, cache_file, overwrite):
        try:
            TestRebuild._delete_cache(str(cache_file))
        except FileNotFoundError:
            pass
        except:
            raise

        context = Context()
        context.archive = archive_dir
        context.cache = cache_file
        context.data = os.path.join(get_data_path(), 'iris.csv')
        context.overwrite = overwrite
        context.schema = SortedDict({'0': 'Name'})

        init(context)
        archive(context)

        expected_frame = DataFrame(read_csv(context.data, dtype=str))

        if context.overwrite:
            with open(str(context.cache), mode='w') as f:
                f.write('content')

        rebuild(context)

        actual_frame = DataFrame(read_csv(str(context.cache), dtype=str))

        assert_frame_equal(expected_frame, actual_frame)

    def test_rebuild_iris_no_schema(self, archive_dir, cache_file, overwrite):
        try:
            TestRebuild._delete_cache(str(cache_file))
        except FileNotFoundError:
            pass
        except:
            raise

        context = Context()
        context.archive = archive_dir
        context.cache = cache_file
        context.data = os.path.join(get_data_path(), 'iris.csv')
        context.overwrite = overwrite
        context.schema = SortedDict()

        archive(context)

        expected_frame = DataFrame(read_csv(context.data, dtype=str))

        if context.overwrite:
            with open(str(context.cache), mode='w') as f:
                f.write('content')

        rebuild(context)

        actual_frame = DataFrame(read_csv(str(context.cache), dtype=str))

        assert_frame_equal(expected_frame, actual_frame)

    def test_rebuild_fileexistserror(self, archive_dir, cache_file):
        try:
            TestRebuild._delete_cache(str(cache_file))
        except FileNotFoundError:
            pass
        except:
            raise

        context = Context()
        context.archive = archive_dir
        context.cache = cache_file
        context.data = os.path.join(get_data_path(), 'iris.csv')
        context.overwrite = False
        context.schema = SortedDict()

        archive(context)

        with open(str(context.cache), mode='w') as f:
            f.write('content')

        with pytest.raises(FileExistsError):
            rebuild(context)
