#!/usr/bin/env python 

# This command line interface for ge.tt to upload files provides zipping 
# facility when compared to the source code

__AUTHOR__ = "Madhukar Sriramu"
__EMAIL__ = "madhusirmv@gmail.com"
__DATA__ = "2016/08/01"
__ORIGINAL_AUTHOR__ = "Prakhar Srivastav"
__SOURCE__ = "https://github.com/prakhar1989/gettup/blob/master/gett.py"
__version__ = "1"

import sys
import os
import requests
import json
import argparse
import signal
import getpass
import zipfile

LOGIN_URL = "https://open.ge.tt/1/users/login"
SHARE_URL = "https://open.ge.tt/1/shares/create?accesstoken="
VERBOSE = True
CONFIG_FILE = '.gett.cfg'

def signalhandler(signal, frame):
    """ Signal handler """
    print("Graceful exit\n");
    sys.exit(0)

def log(msg):
    """ print to stdout """
    print(msg)

def config_file():
    """ Set the name of the config file """
    home = os.getenv("HOME")
    return os.path.join(home, CONFIG_FILE)

def read_config(token):
    """ Read the value of a particular token """
    file_location = config_file()

    if sys.version_info[0] == 3:
        import configparser as cp
    else:
        import ConfigParser as cp
    config = cp.RawConfigParser()
    if not config.read(file_location) or not config.has_option('TOKENS', token) \
            or not config.has_section('TOKENS'):
        print "Entered"
        return None

    return config.get('TOKENS', token)

def write_config(json):
    """ Write key, values to a config file on disk """
    if sys.version_info[0] == 3:
        import configparser as cp
    else:
        import ConfigParser as cp
    config = cp.RawConfigParser()
    config.add_section("TOKENS")
    for k in json:
        config.set("TOKENS", k, json[k])
    file_on_disk = config_file()
    with open(file_on_disk, 'w') as f:
        config.write(f)

def setup_tokens():
    """ Get access token by API """

    email = raw_input("Please enter your account email address: ")
    password = getpass.getpass("Please enter your password: ") # Similar to stty -echo
    api_key = raw_input("Please enter your API key: ")
    
    log("Validating credentials...");
    r = requests.post(LOGIN_URL, data=json.dumps({'email': email, 
                                                  'password': password, 
                                                'apikey' : api_key}))
    access_token  = r.json().get('accesstoken')
    refresh_token = r.json().get('refreshtoken')
    if not access_token or not refresh_token:
        print "Error! Your credentials failed validation. Exiting program"
        sys.exit(0)
    log("Credentials verified...")
    # add the tokens to a config file
    write_config({"accesstoken": access_token, "refreshtoken": refresh_token})
    return access_token

def create_share(title=None):
    """ Create a new share """
    access_token = get_access_token()

    if title:
        r = requests.post(SHARE_URL + access_token, data=json.dumps({'title': title}))
    else:
        r = requests.post(SHARE_URL + access_token)
   
    if r.status_code != 200:
        # don't know what to do if fails
        print "in here"

    return r.json().get('sharename')

def refresh_access_token():
    """ re-fetches the access token using the refresh token and writes to the 
        config file 
    """
    log("Refreshing the access token...")
    refreshtoken = read_config("refreshtoken")
    r = requests.post(LOGIN_URL, data=json.dumps({'refresh-token': refreshtoken}))
    
    if r.status_code != 200:
        print "Error: cannot fetch refresh token. Try deleting ~/.gett.cfg file and retrying"
        sys.exit(0)

    access_token = r.json.get('accesstoken')
    refresh_token = r.json.get('refreshtoken')

    write_config({'accesstoken': access_token, 'refreshtoken': refresh_token})

def get_access_token():
    """ gets the access token from the saved file or via API query"""
    return read_config('accesstoken') or setup_tokens()

def upload_file(f, share, title):
    """ Upload file to a share if the share exists, else create a share and then 
        upload
    """
    accesstoken = get_access_token()
    file_url = "http://open.ge.tt/1/files/%s/create?accesstoken=%s" % (share, accesstoken)
    log("+ Setting up a file name on the share...")
    r = requests.post(file_url, data=json.dumps({'filename': f}))
    if r.status_code != 200:
        refresh_access_token()
        return upload_file
    get_url = r.json().get("getturl")
    post_url = r.json()['upload']['posturl']
    r = requests.post(post_url, files={'filename': open(f, 'rb')})
    if r.status_code == 200:
        print "Upload successful. The file URL is at " + get_url
    else:
        print "Error: " + r.json().get('error')

def bulk_upload(files, zipfiles, sharename=None, title=None):
    """ What do I need to upload?
        the API key, the user name, and the password
        :param files: list of files to be uploaded
        :param share: optional
        :param title: title of the new share
    """
    share = sharename or create_share()
    # Archive name
    if zipfiles:
        archive = raw_input("Choose archive name to be stored as with a .zip extension: ")
        ziph = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)

    # Upload files iteratively or add to the archive
    for f in files:
        if zipfiles:
            print "+ Archiving " + f
            ziph.write(f)
            continue
        print "Uploading file: " + f
        upload_file(f, share, title)
        log("-------------------------------------------------")

    if zipfiles: 
        print "Uploading archive: " + archive
        upload_file(archive, share, title)

def main():
    """ Start here! """
    signal.signal(signal.SIGINT, signalhandler)

    # Parse arguments
    parser = argparse.ArgumentParser(description='Wrapper application to upload'
                                                ' files to ge.tt')
    
    # File uploads
    file_uploads = parser.add_argument_group("files")
    file_uploads.add_argument("-f", "--files", 
                                    metavar="Files", 
                                    nargs="*", 
                                    help="list of files you want to upload")
    file_uploads.add_argument("-s", "--share", metavar="share_name", 
                                    help="upload files to a particular share")
    file_uploads.add_argument("-t", "--title", metavar="title",
                                    help="title for the new share")
    file_uploads.add_argument("-z", action="store_true",
                                    help="flag to zip files or not")
    args = parser.parse_args()

    zipfiles = True if args.z else False

    if args.files:
        bulk_upload(args.files, zipfiles, sharename=args.share, title=args.title)

    if len(sys.argv) == 1:
        parser.print_help()

if __name__ == "__main__":
    main()
