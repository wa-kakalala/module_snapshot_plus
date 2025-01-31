# coding=utf-8
# original author: QyLey
# modified by: yyrwkk

# from docx import Document
# from docx.oxml.ns import qn
# from docx.shared import Pt, RGBColor  # 导入Pt类和RGBColor类，用于设置字体大小和颜色
# from utils.create_table import create_table

# doc = Document()
# doc.styles['Normal'].font.size = Pt(12)             # 设置默认字号为12号字体(小四)
# doc.styles['Normal'].font.name = 'Times New Roman'  # 设置默认字体为楷体
# doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')  # 设置中文字体为宋体

# # 添加一个5行3列的表格，样式是网格实线
# data = [
#     ["clk","1","I","时钟"],
#     ["rst_n","1","I","复位,低有效"]
# ]
# create_table(doc,data)
# doc.save('./test.docx')

from utils.parse_module import get_module_info
import time

from tkinter import *
# type object 'Image' has no attribute 'new' 问题: https://www.cnblogs.com/relustarry/p/14357476.html
from PIL import Image,ImageDraw,ImageFont

class tk_ui(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry('480x640')
        self.root.title("module_snapshot_plus")

        self.btn = Button(self.root, text='generate', command=self.run)
        self.btn.place(relx=0.4, rely=0.95, relwidth=0.2, relheight=0.05)
        self.root.mainloop()
    def run(self):
        file_path = "./data/add.sv"
        module_info = get_module_info(file_path)
        self.draw(module_info)

    def draw(self,module_info):
        m_name, left_io, right_io, io_info,(hl,ll),(hr,lr) = module_info
        # self.winNew = Toplevel(self.root)
        # self.winNew.title("m_name")
        border_x = 100
        border_y = 20
        line_x = 13
        line_y = 28

        title = m_name
        i = len(title)
        title_ln  = title 
        ln_num  = 0
        line_mid = 0
        if(len(title_ln)>line_mid):
            line_mid = len(title_ln)
        height = line_y*max(hl, hr)
        width = line_x*(2*max(ll,lr)+line_mid+2)
        # self.cv = Canvas(self.winNew,bg = 'white', height = height+border_y*2, width = width+border_x*2)
        image = Image.new('RGB', (width+border_x*2, height+border_y*2), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        # self.cv.create_rectangle(border_x,border_y,width+border_x,height+border_y, fill = 'white', width = 2)
        draw.rectangle((border_x,border_y,width+border_x,height+border_y), outline='black', width=2)

        start_y = (height+border_y*2-ln_num*line_y)/2
        i = 0
        # 加载字体（Courier，15号，粗体）
        try:
            font = ImageFont.truetype("Courier New.ttf", size=15)  # 你可以替换为自己的路径
        except IOError:
            font = ImageFont.load_default()  # 如果加载失败，则使用默认字体
        try:
            font_12 = ImageFont.truetype("Courier New.ttf", size=12)  # 你可以替换为自己的路径
        except IOError:
            font_12 = ImageFont.load_default()  # 如果加载失败，则使用默认字体
        # self.cv.create_text(border_x+width/2,start_y + i*line_y,text=title_ln,fill ='#808080',anchor = "c",font=('Courier', 15, 'bold'))
        draw.text((border_x+width/2,start_y + i*line_y),title_ln,fill ='#808080',anchor = "c",font=font)
        i = 1
        start_y = (height+border_y*2-(hl-1)*line_y)/2
        # lli = list(left_io.keys())
        for s in left_io:
            if left_io[s][0]=='input':
                x0 = border_x+16
                y0 = start_y+i*line_y
                x1 = border_x+4
                y1 = start_y+i*line_y-6
                x2 = border_x+4
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
            elif left_io[s][0]=='output':
                x0 = border_x+4
                y0 = start_y+i*line_y
                x1 = border_x+16
                y1 = start_y+i*line_y-6
                x2 = border_x+16
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
            else:
                x0 = border_x+17
                y0 = start_y+i*line_y
                x1 = border_x+11
                y1 = start_y+i*line_y-6
                x2 = border_x+11
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
                x0 = border_x+3
                y0 = start_y+i*line_y
                x1 = border_x+9
                y1 = start_y+i*line_y-6
                x2 = border_x+9
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
            signal_width = left_io[s][1]
            signal_name = s
            # self.cv.create_text(border_x+20,start_y + i*line_y,text=signal_name,fill ='#000000',anchor = "w",font=('Courier', 15))
            w_width, w_height = draw.textsize(signal_name, font=font)
            draw.text((border_x+20,start_y + i*line_y-w_height/2),signal_name,fill ='#000000',anchor = "w",font=font)
            if signal_width == '1':
                # self.cv.create_line(10,start_y + i*line_y,border_x,start_y + i*line_y,width=2)
                draw.line((10, start_y + i*line_y, border_x, start_y + i*line_y), fill='black', width=2)
            else:
                # self.cv.create_line(10,start_y + i*line_y,border_x,start_y + i*line_y,width=4)
                draw.line((10, start_y + i*line_y, border_x, start_y + i*line_y), fill='black', width=4)
                # self.cv.create_line(20,start_y + i*line_y-5,30,start_y + i*line_y+5,width=2)
                draw.line((20, start_y + i*line_y-5, 30, start_y + i*line_y+5), fill='black', width=2)
                # self.cv.create_text(30,start_y + i*line_y-10,text=signal_width,fill ='#000000',anchor = "w",font=('Courier', 12))
                draw.text((30,start_y + i*line_y-10),str(signal_width),fill ='#000000',anchor = "w",font=font_12)
            i = i+1

        i = 1
        
        start_y = (height+border_y*2-(hr-1)*line_y)/2
        for s in right_io:
            signal_width = right_io[s][1]
            signal_name =  s
            w_width, w_height = draw.textsize(signal_name, font=font)
            # self.cv.create_text(width+border_x-20,start_y + i*line_y,text=signal_name,fill ='#000000',anchor = "e",font=('Courier', 15))
            draw.text((width+border_x-20-w_width,start_y + i*line_y-w_height/2),signal_name,fill ='#000000',anchor = "mm",font=font)
            if right_io[s][0]=='input':
                    x0 = width+border_x-16
                    y0 = start_y+i*line_y
                    x1 = width+border_x-4
                    y1 = start_y+i*line_y-6
                    x2 = width+border_x-4
                    y2 = start_y+i*line_y+6
                    # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                    draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
            elif right_io[s][0]=='output':
                x0 = width+border_x-4
                y0 = start_y+i*line_y
                x1 = width+border_x-16
                y1 = start_y+i*line_y-6
                x2 = width+border_x-16
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
            else:
                x0 = width+border_x-17
                y0 = start_y+i*line_y
                x1 = width+border_x-11
                y1 = start_y+i*line_y-6
                x2 = width+border_x-11
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')
                x0 = width+border_x-3
                y0 = start_y+i*line_y
                x1 = width+border_x-9
                y1 = start_y+i*line_y-6
                x2 = width+border_x-9
                y2 = start_y+i*line_y+6
                # self.cv.create_polygon(x0, y0, x1, y1, x2, y2,fill ='#c0c0c0')
                draw.polygon([(x0, y0), (x1, y1), (x2, y2)], fill='#c0c0c0')

            if signal_width == '1':
                # self.cv.create_line(width+2*border_x-10,start_y + i*line_y,width+border_x,start_y + i*line_y,width=2)
                draw.line((width+2*border_x-10,start_y + i*line_y,width+border_x,start_y + i*line_y), fill='black', width=2)
            else:
                # self.cv.create_line(width+2*border_x-10,start_y + i*line_y,width+border_x,start_y + i*line_y,width=4)
                draw.line((width+2*border_x-10,start_y + i*line_y,width+border_x,start_y + i*line_y), fill='black', width=4)
                # self.cv.create_line(width+border_x+20,start_y + i*line_y-5,width+border_x+30,start_y + i*line_y+5,width=2)
                draw.line((width+border_x+20,start_y + i*line_y-5,width+border_x+30,start_y + i*line_y+5), fill='black', width=2)
                # self.cv.create_text(width+border_x+30,start_y + i*line_y-10,text=signal_width,fill ='#000000',anchor = "w",font=('Courier', 12))   
                draw.text((width+border_x+30,start_y + i*line_y-10),str(signal_width),fill ='#000000',anchor = "w",font=font_12)
            i = i+1

        image.save(m_name+".png")
        



if __name__ == '__main__':
    ui = tk_ui()