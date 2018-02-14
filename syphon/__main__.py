"""syphon.__main__.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
def _main(argv: list) -> int:
    """Main entry point.
    
    Returns:
        int: An integer exit code. `0` for success or `1` for failure.
    """
    from os.path import abspath, join
    from sortedcontainers import SortedDict

    from syphon.rebuild import rebuild
    from syphon.archive import archive
    from syphon.init import init
    from syphon.schema import load

    from .__version__ import __version__
    from . import Context, get_parser

    parser = get_parser()
    args = parser.parse_args(argv[1:])

    this_context = Context()

    if args.version is True:
        print(__version__)
        return 0

    this_context.overwrite = args.force
    this_context.verbose = args.verbose

    if getattr(args, 'data', False):
        this_context.data = abspath(args.data)

    if getattr(args, 'destination', False):
        if getattr(args, 'rebuild', False):
            this_context.cache = abspath(args.destination)
        else:
            this_context.archive = abspath(args.destination)

    if getattr(args, 'headers', False):
        this_context.schema = SortedDict()
        index = 0
        for h in args.headers:
            this_context.schema['{}'.format(index)] = h
            index += 1

    if getattr(args, 'source', False):
        this_context.archive = abspath(args.source)

    if getattr(args, 'metadata', False):
        if args.metadata is not None:
            this_context.meta = abspath(args.metadata)

    try:
        if getattr(args, 'archive', False):
            schemafile = join(this_context.archive, this_context.schema_file)
            this_context.schema = load(schemafile)
            archive(this_context)

        if getattr(args, 'init', False):
            init(this_context)

        if getattr(args, 'rebuild', False):
            rebuild(this_context)
    except OSError as err:
        print(str(err))
        return 1

    return 0

if __name__ == '__main__':
    from sys import argv

    # import pandas as pd
    # from pandas import concat, DataFrame, Series
    # from pandas.util.testing import makeCustomIndex
    # from sortedcontainers import SortedDict
    # from syphon.tests import make_dataframe

    # from syphon.archive import datafilter

    # def build(frame, meta_cvals, keylist, result=[]):
    #     this_keylist = keylist.copy()
    #     this_keylist.reverse()
    #     header = None
    #     try:
    #         header = this_keylist.pop()
    #     except IndexError:
    #         result.append(frame)
    #         return result
    #     except:
    #         raise

    #     for val in meta_cvals[header]:
    #         rows, _ = frame.shape
    #         new_col = Series([val]*rows, name=header)
    #         this_frame = concat([frame.copy(), new_col], axis=1)
    #         try:
    #             result = build(this_frame, meta_cvals, this_keylist, result=result)
    #         except:
    #             raise
    #     return result

    # def test(rows, cols, metadata_columns):
    #     frame = make_dataframe(rows, cols)
    #     meta_cvals = metadata_columns.copy()
    #     keylist = list(meta_cvals.keys())

    #     expected = build(frame, meta_cvals, keylist)

    #     schema = SortedDict()
    #     index = 0
    #     for k in keylist:
    #         schema[str(index)] = k
    #         index += 1

    #     alldata = DataFrame()
    #     for f in expected:
    #         alldata = concat([alldata, f])
    #     alldata.reset_index(drop=True, inplace=True)

    #     actual = datafilter(schema, alldata)

    #     for e in expected:
    #         match = None
    #         for a in actual:
    #             if e.equals(a):
    #                 match = a.copy()
    #                 break
    #         if match is not None:
    #             print('found a match!')
    #             print(e)
    #             print(match)
    #         else:
    #             print('no matches!')

    #     return 0

    # test(5,2,{})
    # test(6,2,{})
    # exit(0)

    exit(_main(argv))
