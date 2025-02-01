# coding=utf-8
# original author: QyLey
# modified by: yyrwkk
from utils.create_table import create_table
from utils.parse_module import get_module_info
from utils.insert_mdpic import insert_mdpic
from utils.draw_module import draw_module

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor  # 导入Pt类和RGBColor类，用于设置字体大小和颜色

import os
from tkinter import *
from tkinter import filedialog
import datetime

class tk_ui(object):
    module_file_name_list = []
    module_file_path_list = []
    file_all_right = True
    def __init__(self):
        self.root = Tk()
        self.root.geometry('320x480')
        self.root.title("module_snapshot_plus")

        self.btn_load = Button(self.root, text='load', command=self.load_func)
        self.btn_load.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.05)

        self.log = Text(self.root) 
        self.log.place(relx = 0.05, rely = 0.15, relheight= 0.65, relwidth=0.9)

        self.btn_gen = Button(self.root, text='generate', command=self.gen_func)
        self.btn_gen.place(relx=0.4, rely=0.9, relwidth=0.2, relheight=0.05)

        self.root.mainloop()
    def load_func(self):
        self.log.delete(1.0, END)
        file_path = filedialog.askopenfilename(initialdir='./', title="select filelistfile")
        if not file_path:
            self.log.insert(END, "no file selected")
            return
        if not os.path.isfile(file_path):
            self.log.insert(END, "this is not a file")
            return
        self.module_file_name_list = []
        self.module_file_path_list = []
        self.file_all_right = True
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not os.path.isfile(line):
                    self.log.insert(END, "file not exist: " + line)
                    self.file_all_right = False
                else:
                    self.module_file_name_list.append(os.path.basename(line))
                    self.module_file_path_list.append(line)
        if not self.file_all_right :
            return 
               
        for file_name in self.module_file_name_list:
            self.log.insert(END, file_name + "\n")
        
    def gen_func(self):
        if os.path.exists("./temp"):
            file_list = os.listdir("./temp")
            for file in file_list:
                file_path = os.path.join("./temp", file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.mkdir("./temp")
        if not os.path.exists("./output"):
            os.mkdir("./output")
        doc = Document()
        doc.styles['Normal'].font.size = Pt(12)             # 设置默认字号为12号字体(小四)
        doc.styles['Normal'].font.name = 'Times New Roman'  # 设置默认字体为楷体
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')  # 设置中文字体为宋体

        for i in range(len(self.module_file_path_list)):
            file_path = self.module_file_path_list[i]
            module_info = get_module_info(file_path)
            doc.add_heading(f'1.{i+1} {module_info[0]}', level=2)
            pic_path = draw_module(module_info,"./temp/")
            insert_mdpic(doc,pic_path,module_info[0])
            create_table(doc,module_info[3],tb_name=module_info[0])
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        doc_file_name = './module_info_' + now + '.docx'
        doc.save("./output/" + doc_file_name)
        self.log.insert(END, "finish: " + doc_file_name + " !" + "\n")

if __name__ == '__main__':
    ui = tk_ui()