import uuid
import os
import sys
import client
import threading
def test_case_1(N):
    """
    Test case 1
    client N can be 2, 4, 8, 16
    thread = 10

    :return:
    """
    #获取下载文件列表
    file_list=client.get_file_list()['data']

    client_id = "measure_1_client_"+str(N)
    #人工拼凑一个argparse.ArgumentParser()读取命令行后的args
    args = type("args", (object,), {})()
    args.func = "download_file"
    args.client_id = client_id
    args.sign_filename = None
    args.multi_filename = str(file_list)
    args.multithread = "N"
    #按照N，启动N个线程并发执行main函数
    for i in range(N):
        t = threading.Thread(target=client.main, args=(args,))
        t.start()




def test_case_2():
    pass

if __name__ == '__main__':
    test_case_1()
    test_case_2()
    print("All test cases passed!")