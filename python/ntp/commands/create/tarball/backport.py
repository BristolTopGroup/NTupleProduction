import os
try:
    from pwd import getpwnam
except ImportError:
    getpwnam = None

try:
    from grp import getgrnam
except ImportError:
    getgrnam = None

def _get_gid(name):
    """Returns a gid, given a group name."""
    if getgrnam is None or name is None:
        return None
    try:
        result = getgrnam(name)
    except KeyError:
        result = None
    if result is not None:
        return result[2]
    return None

def _get_uid(name):
    """Returns an uid, given a user name."""
    if getpwnam is None or name is None:
        return None
    try:
        result = getpwnam(name)
    except KeyError:
        result = None
    if result is not None:
        return result[2]
    return None

def _make_tarball(base_name, base_dir, compress="gzip", verbose=0, dry_run=0,
                  owner=None, group=None, logger=None):
    """Create a (possibly compressed) tar file from all the files under
    'base_dir'.

    'compress' must be "gzip" (the default), "bzip2", or None.

    'owner' and 'group' can be used to define an owner and a group for the
    archive that is being built. If not provided, the current owner and group
    will be used.

    The output tar file will be named 'base_name' +  ".tar", possibly plus
    the appropriate compression extension (".gz", or ".bz2").

    Returns the output filename.
    """
    tar_compression = {'gzip': 'gz', 'bzip2': 'bz2', None: ''}
    compress_ext = {'gzip': '.gz', 'bzip2': '.bz2'}

    # flags for compression program, each element of list will be an
    # argument
    if compress is not None and compress not in compress_ext.keys():
        raise ValueError, \
            ("bad value for 'compress': must be None, 'gzip' or 'bzip2'")

    archive_name = base_name + '.tar' + compress_ext.get(compress, '')
    archive_dir = os.path.dirname(archive_name)

    if not os.path.exists(archive_dir):
        if logger is not None:
            logger.info("creating %s", archive_dir)
        if not dry_run:
            os.makedirs(archive_dir)

    # creating the tarball
    import tarfile  # late import so Python build itself doesn't break

    if logger is not None:
        logger.info('Creating tar archive')

    uid = _get_uid(owner)
    gid = _get_gid(group)

    def _set_uid_gid(tarinfo):
        if gid is not None:
            tarinfo.gid = gid
            tarinfo.gname = group
        if uid is not None:
            tarinfo.uid = uid
            tarinfo.uname = owner
        return tarinfo

    if not dry_run:
        tar = tarfile.open(archive_name, 'w|%s' %
                           tar_compression[compress])
        try:
            tar.add(base_dir)
        except:
            if logger is not None:
                logger.error('Error while creating the tar file')
        finally:
            tar.close()

    return archive_name
_ARCHIVE_FORMATS = {
    'gztar': (_make_tarball, [('compress', 'gzip')], "gzip'ed tar-file"),
    'bztar': (_make_tarball, [('compress', 'bzip2')], "bzip2'ed tar-file"),
    'tar':   (_make_tarball, [('compress', None)], "uncompressed tar file"),
}


def make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0,
                 dry_run=0, owner=None, group=None, logger=None):
    """Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "bztar"
    or "gztar".

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    save_cwd = os.getcwd()
    if root_dir is not None:
        if logger is not None:
            logger.debug("changing into '%s'", root_dir)
        base_name = os.path.abspath(base_name)
        if not dry_run:
            os.chdir(root_dir)

    if base_dir is None:
        base_dir = os.curdir

    kwargs = {'dry_run': dry_run, 'logger': logger}

    try:
        format_info = _ARCHIVE_FORMATS[format]
    except KeyError:
        raise ValueError, "unknown archive format '%s'" % format

    func = format_info[0]
    for arg, val in format_info[1]:
        kwargs[arg] = val

    if format != 'zip':
        kwargs['owner'] = owner
        kwargs['group'] = group

    try:
        filename = func(base_name, base_dir, **kwargs)
    finally:
        if root_dir is not None:
            if logger is not None:
                logger.debug("changing back to '%s'", save_cwd)
            os.chdir(save_cwd)

    return filename
