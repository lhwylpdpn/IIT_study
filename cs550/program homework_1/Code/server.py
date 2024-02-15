from flask import Flask, send_file,g,request,make_response,Response
import configparser
import os
import json
import uuid
import time
import hashlib
app = Flask(__name__)

def read_config():
    config = configparser.ConfigParser()
    config.read('server_config.conf', encoding='utf-8')
    return config

def log(content):
    #判断是否存在日志文件
    log_file='server.log'
    if not os.path.exists(log_file):
        with open(log_file,'w') as f:
            f.write(content+'\n')
    else:
        with open(log_file,'a') as f:
            f.write(content+'\n')

@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()

@app.after_request
def after_request(response):
    total_time = time.time() - g.start_time
    if 'download' in request.url:
        api_name = request.url

        # log: request_id,client_id，client_IP，api_name，filesize,api_time,api_status
        log_content = {'request_id': g.request_id, 'client_id': request.headers.get('client_id'), 'client_IP': request.remote_addr,
                       'api_name': api_name,
                       'filesize': response.content_length, 'api_time': total_time, 'api_status': response.status_code}
        log(json.dumps(log_content, ensure_ascii=False))
    return response

@app.route('/download/<filename>')
def download_file(filename):

    config = read_config()
    file_dir = config.get('server', 'file_dir')
    if not os.path.exists(file_dir+"/"+filename):

        return Response('file not found', status=400)
    else:
        with open(file_dir+"/"+filename, 'rb') as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        md5_hash = file_hash.hexdigest()
        response = make_response(send_file(file_dir+"/"+filename, as_attachment=True))
        response.headers['X-MD5'] = md5_hash  # 将 MD5 哈希值添加到响应头中
        return response


@app.route('/get_file_list/')
def get_list():
    try:
        config = read_config()
        file_dir = config.get('server', 'file_dir')
        file_dir = os.path.abspath(file_dir)
        file_list = os.listdir(file_dir)
        if not file_list:
            res={'status':1002,'msg':'file not found'}
            res=json.dumps(res,ensure_ascii=False)
            return res
        res={'status':200,'msg':'success','data':file_list}
        res=json.dumps(res,ensure_ascii=False)
        return res
    except Exception as e:
        res={'status':1001,'msg':'error','data':str(e)}
        return res

if __name__ == '__main__':
    app.run()