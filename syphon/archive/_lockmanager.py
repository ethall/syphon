"""syphon.archive._lockmanager.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
from os.path import abspath

class LockManager(object):
    """Lock file helper.
    
    A lock file is any file named `#lock`. Lock files allow communication
    between programs with lock file support to prevent the removal of files
    that may be in use.
    """
    def __init__(self):
        self._locks = list()

    @property
    def filename(self):
        """Lock file name."""
        return '#lock'

    @staticmethod
    def _delete(filepath: str):
        """Delete a given file."""
        from os import remove
        
        try:
            remove(filepath)
        except:
            raise

    @staticmethod
    def _touch(filepath: str):
        """Linux touch-like command."""
        from os import utime

        try:
            with open(filepath, 'a'):
                utime(filepath, None)
        except:
            raise

    def lock(self, path: str) -> str:
        """Create a lock file in a given directory.

        Args:
            path (str): Directory to lock.

        Returns:
            str: Absolute filepath of the created lock file.
        """
        from os.path import join

        filepath = join(abspath(path), self.filename)

        try:
            LockManager._touch(filepath)
        except:
            raise
        else:
            if filepath not in self._locks:
                self._locks.append(filepath)

        return filepath

    def release(self, filepath: str):
        """Remove the given lock file.

        Args:
            filepath (str): Location of a lock file.
        """
        fullpath = abspath(filepath)

        if fullpath in self._locks:
            self._locks.remove(fullpath)
            try:
                LockManager._delete(fullpath)
            except FileNotFoundError:
                pass
            except:
                raise
