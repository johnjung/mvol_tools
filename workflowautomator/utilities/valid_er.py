import re
import json
from password import ocpassword
import owncloud
import os
import requests
from mvol_validator import mainvalidate
from random import shuffle
#from queue_er import allreadies


def filterbottom(oc, p):
    if re.match('mvol/\d{4}/\d{4}/\d{4}/?$', p):
        return ('IIIF_Files/' + p, p)
    elif not p:
        return


def runutil(oc, file_info, result):
    for entry in oc.list(file_info.get_path()):
        if entry.get_name() in ('valid', 'invalid'):
            oc.delete(entry)
    os.utime(result)
    oc.put_file(file_info, result)

username = "ldr_oc_admin"
password = ocpassword
oc = owncloud.Client('https://s3.lib.uchicago.edu/owncloud')
oc.login(username, password)

r = requests.get('https://www2.lib.uchicago.edu/keith/tmp/cai.json')
r = r.json()
allqueues = r['none'] + r['valid'] + r['invalid'] + r['ready'] + r['queue']
#allqueues = [(30, 'mvol/0001/0002/0000')]
#allqueues = [(30, 'mvol/0002/0010/0004')]
shuffle(allqueues)
allqueuesfiltered = []
for rt in allqueues:
    print(rt)
    allqueuesfiltered = allqueuesfiltered + [filterbottom(oc, rt[1])]
unknowns = []
for rt in allqueuesfiltered:
    if rt:
        print(rt[0])
        freshbatcherrors = mainvalidate(oc, rt[0])
        if not freshbatcherrors:
            runutil(oc, oc.file_info(rt[0]), "valid")
            print("no error")
        else:
            f = open("invalid", "w")
            for error in freshbatcherrors:
                print(error)
                if error[-22:] == "has an unknown error.\n":
                    unknowns.append(error)
                f.write(error)
            f.close()
            runutil(oc, oc.file_info(rt[0]), "invalid")

print("unknowns:\n")
for u in unknowns:
    print(u)