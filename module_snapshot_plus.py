# encoding: utf-8

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor  # 导入Pt类和RGBColor类，用于设置字体大小和颜色
from utils.create_table import create_table

doc = Document()
doc.styles['Normal'].font.size = Pt(12)             # 设置默认字号为12号字体(小四)
doc.styles['Normal'].font.name = 'Times New Roman'  # 设置默认字体为楷体
doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')  # 设置中文字体为宋体

# 添加一个5行3列的表格，样式是网格实线
data = [
    ["clk","1","I","时钟"],
    ["rst_n","1","I","复位,低有效"]
]
create_table(doc,data)
doc.save('./test.docx')

