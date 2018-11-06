"""Usage:
    mvol_check_sync.py (--owncloud-to-development | --owncloud-to-production) (--list-in-sync | --list-out-of-sync) <identifier> ...
"""

from docopt import docopt
import operator
import paramiko
import stat
import sys


def get_path_owncloud(identifier):
    """Return a path for a given identifier."""
    return '/data/voldemort/digital_collections/data/ldr_oc_admin/files/IIIF_Files/{}'.format(identifier.replace('-', '/'))

def get_path_xtf_development(identifier):
    """Return a path for a given identifier."""
    return '/usr/local/apache-tomcat-6.0/webapps/xtf/data/bookreader/{}'.format(identifier)

def get_path_xtf_production(identifier):
    """Return a path for a given identifier."""
    return '/usr/local/apache-tomcat-6.0/webapps/campub/data/bookreader/{}'.format(identifier)

def get_newest_modification_time_from_directory(ftp, directory):
    """ Helper function for get_newest_modification_time. 
        Recursively searches subdirectories for the newest modification time. 
     
        Arguments:
           ftp           -- paramiko ftp instance
	   path_function -- one of get_path_owncloud, get_path_xtf_development,
                            get_path_xtf_production
           identifier    -- e.g. .mvol-0001-0002-0003

        Returns:
           unix timestamp. 
    """

    mtimes = []
    for entry in ftp.listdir_attr(directory):
        if stat.S_ISDIR(entry.st_mode):
            mtime = get_newest_modification_time_from_directory(ftp, '{}/{}'.format(directory, entry.filename))
        else:
            try:
                mtimes.append(entry.st_mtime)
            except FileNotFoundError:
                sys.stderr.write(directory + '\n')
                raise FileNotFoundError

    if mtimes:
        return max(mtimes)
    else:
        return 0

def get_newest_modification_time(ftp, path_function, identifier):
    """Get the most recent modification time for the files associated with a given identifier. 
 
       Arguments:
           ftp           -- paramiko ftp instance
	   path_function -- one of get_path_owncloud, get_path_xtf_development,
                            get_path_xtf_production
           identifier    -- e.g. .mvol-0001-0002-0003

        Returns:
           unix timestamp. 
    """

    return get_newest_modification_time_from_directory(ftp, path_function(identifier))


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['--owncloud-to-development']:
        xtf_server = 'campub-xtf.lib.uchicago.edu'
        xtf_path_function = get_path_xtf_development
    elif args['--owncloud-to-production']:
        xtf_server = 'xtf.lib.uchicago.edu'
        xtf_path_function = get_path_xtf_production
    else:
        raise NotImplementedError

    owncloud_username = ''
    xtf_username = ''

    owncloud_password = ''
    xtf_password = ''

    owncloud_ssh = paramiko.SSHClient()
    owncloud_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    owncloud_ssh.connect('s3.lib.uchicago.edu', username=owncloud_username, password=owncloud_password)
    owncloud_ftp = owncloud_ssh.open_sftp()

    xtf_ssh = paramiko.SSHClient()
    xtf_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    xtf_ssh.connect(xtf_server, username=xtf_username, password=xtf_password)
    xtf_ftp = xtf_ssh.open_sftp()

    if args['--list-in-sync']:
        comparison = operator.lt
    elif args['--list-out-of-sync']:
        comparison = operator.gt
    else:
        raise NotImplementedError

    for identifier in args['<identifier>']:
        try:
            if comparison(
                get_newest_modification_time(owncloud_ftp, get_path_owncloud, identifier),
                get_newest_modification_time(xtf_ftp, xtf_path_function, identifier)
            ):
                print(identifier)
        except FileNotFoundError:
            if args['--list-out-of-sync']: 
                print(identifier)
