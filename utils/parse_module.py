# coding = utf-8
# original author: QyLey
# modified by: yyrwkk
import re

def find_len(content):
    h = 2
    l = [10]
    lv = 1
    lli = list(content.keys())
    for m in lli:
        h = h + 1
        l.append(lv+len(m)+1)
    return h, max(l)
     
def read_line(s):
    ln = s.strip() # 去除两侧的空白字符
    ln = re.sub(r" logic ", " ", ln) # 去除logic关键字
    ln = re.sub(r" wire ", " ", ln)  # 去除wire关键字
    ln = re.sub(r" reg ", " ", ln)   # 去除reg关键字
    t = None
    sig = []
    mname = ""
    # state 1
    divided = re.split(r"[>[\s]",ln,1)
    start_word = divided[0]
    if start_word == 'input':
        t = "signal"
        sig_io = 'input'
        ln = divided[1]
    elif start_word == 'output':
        t = "signal"
        sig_io = 'output'
        ln = divided[1]
    elif start_word == 'inout':
        t = "signal"
        sig_io = 'inout'
        ln = divided[1]
    elif start_word == 'module':
        t = "module"
        ln = divided[1]

    #state 2
    ln=ln.strip() # 去除两侧的空白字符
    if t == 'signal':
        ssss=re.search('^\[.*:.*\]?',ln)
        if ssss:
            higher = re.search('^\[.*?:',ssss.group()).group()
            lower = re.search(':.*?\]',ssss.group()).group()
            try:
                sig_wid = int(eval(higher[1:-1] + '-' + lower[1:-1] + '+1'))
            except:
                sig_wid = higher[1:-1]
            divided = re.split(r"[,\s]",ln,1)
            ln = divided[1]
        else:
            sig_wid = '1'
    elif t == 'module':
        divided = re.split(r"[#\(\s]",ln,1)
        mname = divided[0].strip()

    #stage 3
    ln=ln.strip() # 去除两侧的空白字符
    if t == 'signal':
        divided = re.split(r"[,\s\)]",ln,1)
        sig_name = divided[0].strip()
        if sig_name == ']':
            ln = divided[1].strip()
            divided = re.split(r"[,\s\)]",ln,1)
            sig_name = divided[0].strip()
        sig = [sig_name, sig_io, sig_wid]
    return [t, sig, mname]

def get_module_info(file_path):
    i = 0
    t_last = None
    m_name    = ""
    left_io   = {}  # 将输入放在左侧
    right_io  = {}  # 将输出放在右侧
    io_info   = []  # 信号名,位宽,I/O,描述
    if_end    = False
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            line =re.sub(r"//.*", "", line)
            if len(line) == 0:
                continue
            end_flag = re.findall(r"\)\s*;", line)
            if len(end_flag) > 0:
                if line.startswith(")"):
                    break
                else:   
                    [t, sig, mname] =  read_line(line)
                    if_end = True
            else:
                [t, sig, mname] =  read_line(line)
            
            if t == 'module':
                m_name = mname
            elif t == 'signal':
                io_info.append([sig[0],sig[2],"O" if sig[1] == 'output' else "I",""])

                if sig[1] in ['output']:
                    right_io[sig[0]] = [sig[1],sig[2]]
                else:
                    left_io[sig[0]] = [sig[1],sig[2]]

            if if_end:
                break
    hl, ll = find_len(left_io)
    hr, lr = find_len(right_io)
    return m_name, left_io, right_io, io_info,(hl,ll),(hr,lr)

if __name__ == '__main__':
    file_path = "../data/add.sv"
    m_name, left_io, right_io, io_info ,l_range, r_range = get_module_info(file_path)
    print(m_name)
    print(left_io)
    print(right_io)
    print(io_info)
    print(l_range) 
    print(r_range)

    
            
    

