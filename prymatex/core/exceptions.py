# coding: utf-8

from prymatex.utils.i18n import ugettext as _

class AlreadyRunningError(Exception):
    pass

    
class UnsupportedPlatformError(Exception):
    pass

    
class APIUsageError(Exception):
    '''
    Thrown when something is violating the way Prymatex is meant to be used
    '''
    pass


class PrymatexIOException(Exception):
    pass


class FileNotSupported(Exception):
    pass