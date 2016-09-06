def get_hdfs_store_base():
    import os
    import getpass
    from .. import find_version
    from ntp import NTPROOT

    crab_base = os.path.join(NTPROOT, 'python', 'crab', 'base.py')
    # get crab ntuple version without importing the file
    version = find_version(crab_base)
    group_folder = os.path.join('/hdfs', 'TopQuarkGroup')
    user = getpass.getuser()
    return os.path.join(group_folder, user, version)

HDFS_STORE_BASE = get_hdfs_store_base()
