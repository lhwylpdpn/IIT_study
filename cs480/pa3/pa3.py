# TODO import the necessary classes and methods
import sys
from logic import PropKB
from logic import tt_entails,to_cnf

global broad_X, broad_Y, Additional_info, Query_Sentences
broad_X, broad_Y = 0, 0
Additional_info = []
Query_Sentences = []


def file_read(filename):
    global broad_X, broad_Y
    global Additional_info
    global Query_Sentences

    with open(filename, 'r', encoding='utf-8') as f:
        res = f.readlines()
    tag = 0
    for r in res:
        if 'Board size' in r:
            tag = 1
        if 'Additional Info' in r:
            tag = 2
        if 'Query Sentences' in r:
            tag = 3
        if r[0] == '#':
            continue
        if tag == 1:
            tmp = r.replace('\n', '').lower()
            if 'x' not in tmp:
                print("There is not have x in size,this code can not get the broad's x and y ")
                return
            broad_X = int(tmp.split('x')[0])
            broad_Y = int(tmp.split('x')[1])
        if tag == 2:
            Additional_info.append(r.replace('\n', '').upper())
        if tag == 3:
            Query_Sentences.append(r.replace('\n', '').upper())


def base_kb():
    init_KB = []
    for x in range(0, broad_X):
        for y in range(0, broad_Y):
            _M = []
            _B = []
            if x > 0:
                _M.append("M" + str(x - 1) + str(y))
                _B.append("B" + str(x - 1) + str(y))
            if x + 1 < broad_X:
                _M.append("M" + str(x + 1) + str(y))
                _B.append("B" + str(x + 1) + str(y))
            if y > 0:
                _M.append("M" + str(x) + str(y - 1))
                _B.append("B" + str(x) + str(y - 1))

            if y + 1 < broad_Y:
                _M.append("M" + str(x) + str(y + 1))
                _B.append("B" + str(x) + str(y + 1))

            init_KB.append('B' + str(x) + str(y) + '<=>(' + '|'.join(_M)+')')
            #init_KB.append('M' + str(x) + str(y) + '==>' + '&'.join(_B))
    return init_KB

if __name__ == '__main__':
    #print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    input_file = sys.argv[1]
    file_read(input_file)
    init_clauses = base_kb()
    #print(init_clauses)
    KB = PropKB()
    for S in init_clauses:
        KB.tell(S)
    for S in Additional_info:
        KB.tell(S)
    for S in Query_Sentences:

        print('Yes' if KB.ask_if_true(to_cnf(S)) else 'No')
    #print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))