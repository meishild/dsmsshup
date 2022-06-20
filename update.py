# update.py
import json
import os
import shutil

SRC_BASE_PATH = '/volume1/docker/nginx/ssh/*.icdoit.com'
DES_BASE_PATH = '/usr/syno/etc/certificate'
ARC_BASE_PATH = '/usr/syno/etc/certificate/_archive'

# SRC_BASE_PATH = '.test/ssh-cert'  # 这是步骤3里创建的目录
# DES_BASE_PATH = '.test/certificate'
# ARC_BASE_PATH = '.test/certificate/_archive'
DOMAIN = "*.icdoit.com"


def update(cfg):
    main_domain = DOMAIN
    if DOMAIN.startswith("*."):
        main_domain = DOMAIN.split("*.")[1]

    # [archive_key: (domain_name, destination_path)]
    keys = {}
    # name to key
    for k in cfg:
        for service in cfg[k]['services']:
            name = service['display_name']
            if name.find(main_domain) < 0:
                continue

            cert_name = DOMAIN if DOMAIN.startswith("*.") else name
            keys[k] = {'name': cert_name, 'arc_path': '%s/%s' % (ARC_BASE_PATH, k), 'des_path': [],
                       'src_path': '%s/%s' % (SRC_BASE_PATH, cert_name)}
            # des_path = '%s/%s/%s' %(CERT_BASE_PATH, service['subscriber'], service['service'])
            # print name, des_path
    for k in cfg:
        for service in cfg[k]['services']:
            des_path = '%s/%s/%s' % (DES_BASE_PATH, service['subscriber'], service['service'])
            if os.path.exists(des_path) and k in keys:
                keys[k]['des_path'].append(des_path)
    for key in keys:
        print(keys[key])
        shutil.copy2(keys[key]['src_path'] + '/cert.pem', keys[key]['arc_path'] + '/cert.pem')
        shutil.copy2(keys[key]['src_path'] + '/privkey.pem', keys[key]['arc_path'] + '/privkey.pem')
        shutil.copy2(keys[key]['src_path'] + '/fullchain.pem', keys[key]['arc_path'] + '/fullchain.pem')
        for des in keys[key]['des_path']:
            shutil.copy2(keys[key]['arc_path'] + '/cert.pem', des + '/cert.pem')
            shutil.copy2(keys[key]['arc_path'] + '/privkey.pem', des + '/privkey.pem')
            shutil.copy2(keys[key]['arc_path'] + '/fullchain.pem', des + '/fullchain.pem')


if __name__ == '__main__':
    cfg_str = open('%s/INFO' % ARC_BASE_PATH).read()
    update(json.loads(cfg_str))
