import configparser
import requests
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import time
import os
import json


parser = argparse.ArgumentParser()

# add parser arguments
parser.add_argument("--func", choices=['get_file_list', 'download_file'],help="run function / get_file_list / download_file")
parser.add_argument("--sign_filename", help="when download_file, the file name to download")
parser.add_argument("--client_id", default='none',help="client id")
parser.add_argument("--multi_filename",help="when download_file, the file name to download")
parser.add_argument("--multithread",default='N',choices=['Y', 'N'],help="multi thread download or not")

def log(content):
    log_file='client.log'
    if not os.path.exists(log_file):
        with open(log_file,'w') as f:
            f.write(content+'\n')
    else:
        with open(log_file,'a') as f:
            f.write(content+'\n')

def read_config():
    config = configparser.ConfigParser()
    config.read('client_config.conf', encoding='utf-8')
    return config

def get_file_list():
    config = read_config()
    server_ip = config.get('client', 'server_ip')
    server_port = config.get('client', 'server_port')
    request_url = f'http://{server_ip}:{server_port}/get_file_list/'
    res = requests.get(request_url)
    return res.json()

def download_file(filename,client_id='client1'):
    a=time.time()
    config = read_config()
    server_ip = config.get('client', 'server_ip')
    server_port = config.get('client', 'server_port')
    retry=int(config.get('client', 'retry'))
    request_url = f'http://{server_ip}:{server_port}/download/{filename}'
    headers = {'client_id': client_id}
    while retry>0:
        res = requests.get(request_url, headers=headers)
        client_file_dir = config.get('client', 'file_dir')
        if res.status_code == 200:
            with open(client_file_dir+'/'+filename, 'wb') as f:
                f.write(res.content)
            print('download success')
            # check md5
            md5_hash = res.headers['X-MD5']
            with open(client_file_dir+'/'+filename, 'rb') as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            md5_hash_local = file_hash.hexdigest()
            if md5_hash_local != md5_hash:
                print('md5 check failed, please check the file')
            else:
                print('md5 check success')

            return filename,time.time()-a,'success',None

        else:
            retry=retry-1
            print(res.content.decode('utf-8'))
            print('download failed, retrying...')
    return filename,time.time()-a,'failed',res.content.decode('utf-8')

def main(args):

    if args.func == 'get_file_list':
        res = get_file_list()
        print(res)
    elif args.func == 'download_file':

        #log include client id functionname filename tasktime singetime singel/multi success/fail reason
        client_log={'client_id':'','functionname':'','request_filename':'','download_filename':{},'tasktime':'','singletime':{},'download_type':'','status':{},'reason':{}}
        client_log['client_id']=args.client_id
        client_log['functionname']='download_file'

        if args.sign_filename is None and args.multi_filename is None:
            print('sign_filename and multi_filename is required')
            sys.exit(1)
        elif args.sign_filename is not None:
            a = time.time()
            res_name,singletime,status,reason=download_file(args.sign_filename, args.client_id)
            client_log['request_filename']=args.sign_filename
            client_log['tasktime']=time.time()-a
            client_log['singletime'][args.sign_filename]=singletime
            client_log['download_type']='single'
            client_log['status'][args.sign_filename]=status
            client_log['reason'][args.sign_filename]=reason
            client_log['download_filename'][args.sign_filename]=res_name

        elif args.multi_filename is not None:
            try:

                file_list = eval(args.multi_filename)
                if args.multithread == 'N':
                    a = time.time()
                    client_log['request_filename'] = args.multi_filename
                    client_log['download_type'] = 'single'

                    for file in file_list:
                        res_name,singletime,status,reason=download_file(file, args.client_id)

                        client_log['singletime'][file] = singletime
                        client_log['status'][file] = status
                        client_log['reason'][file] = reason
                        client_log['download_filename'][file] = res_name
                    client_log['tasktime'] = time.time() - a
                if args.multithread == 'Y':
                    threads = []
                    a = time.time()
                    client_log['request_filename'] = args.multi_filename
                    client_log['download_type'] = 'multithread'
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        futures = {executor.submit(download_file, file, args.client_id): file for file in file_list}
                        for future in futures:
                            file = futures[future]

                            res_name,singletime,status,reason=future.result()
                            client_log['singletime'][file] = singletime
                            client_log['status'][file] = status
                            client_log['reason'][file] = reason
                            client_log['download_filename'][file] = res_name

                    client_log['tasktime'] = time.time() - a



            except Exception as e:
                print(e, 'multi_filename format error, should be a list')

        log(json.dumps(client_log))



if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    print(type(args))
    main(args)