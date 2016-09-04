import getpass
import os
from crab.base import __version__

HDFS_STORE_BASE = os.path.join(
    '/hdfs',
    'TopQuarkGroup',
    getpass.getuser(),
    __version__
)
