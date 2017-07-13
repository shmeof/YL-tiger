#!/usr/bin/env python
#coding=utf8

import sys
import win32file
import win32con

reload(sys)
sys.setdefaultencoding('utf-8')

import threading
import os, time
import tkMessageBox
import time
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))

from Tkinter import *
from ScrolledText import ScrolledText  # 文本滚动条x

# ================== 全局配置 ==================
# 监听文件夹
dir_work = 'D:\\YL-tiger'
path_to_watch = dir_work + '\\working'
xls_template = dir_work + '\\template\\Rechnung_Template.xls'

# ================== 全局变量 ==================
global WORKING
WORKING = False

def getPValue(pvalue):
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    to_para = '<para autoLeading="off" fontsize=12 align=center><b><font face="msyh" color=blue>%s</font></b><br/><br/></para>' %(pvalue.decode(encoding='utf-8'))
    return Paragraph(to_para, normalStyle)

# ================================ 转成PDF：方法2 ================================
def outPDF(pdfoutpath,
        dingdanhao,
        time,
        address,
        aclass_values,
        bmenge_values,
        gesamtbetrag_values,
        gesamtbetrag_aritikel_values,
        biscount,
        yunprices,
        guanggaoprices,
        totalprice_value):

    # 表格数据：用法详见reportlab-userguide.pdf中chapter 7 Table
    # http://www.reportlab.com/docs/reportlab-userguide.pdf
    story=[]
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    s1 = "EKEY TECHNOLOGY Co., Ltd."
    s2 = "15/B, 15/F, CHEUK NANG PLAZA,"
    s3 = "250, HENNESSY ROAD, WANCHAI,"
    s4 = "HONG KONG,999077"
    s5 = "CHINA"
    title_para = '''<para autoLeading="off" fontSize=8 align=center>
        <font face="msyh" fontsize=15 color=black><b>%s</b></font><br/><br/>
        <font face="msyh" fontsize=12 color=black><b>%s</b></font><br/>
        <font face="msyh" fontsize=12 color=black>%s</font><br/>
        <font face="msyh" fontsize=12 color=black>%s</font><br/>
        <font face="msyh" fontsize=12 color=black>%s</font><br/><br/>
        </para>''' %(s1, s2, s3, s4, s5)
    title_p = Paragraph(title_para, normalStyle)
    rechnung = "Rechnung"
    rechnung_para = '<para autoLeading="off" fontsize=13 align=center><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(rechnung)
    rechnung_p = Paragraph(rechnung_para, normalStyle)
    to = "To:"
    to_para = '<para autoLeading="off" fontsize=13 align=center><br/><strong><font face="msyh">%s</font></strong><br/><br/></para>' %(to)
    to_p = Paragraph(to_para, normalStyle)
    bestellnummer = "Bestellnummer:"
    bestellnummer_para = '<para autoLeading="off" fontsize=13 align=center><b><font face="msyh">%s</font></b><br/><br/></para>' %(bestellnummer)
    bestellnummer_p = Paragraph(bestellnummer_para, normalStyle)

    bestellnr = "Bestellnr"
    bestellnr_para = '<para autoLeading="off" fontsize=13 align=center><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(bestellnr)
    bestellnr_p = Paragraph(bestellnr_para, normalStyle)
    produktdetails = "Produktdetails"
    produktdetails_para = '<para autoLeading="off" fontsize=13 align=center><b><font face="msyh">%s</font></b><br/><br/></para>' %(produktdetails)
    produktdetails_p = Paragraph(produktdetails_para, normalStyle)
    menge = "Menge"
    menge_para = '<para autoLeading="off" fontsize=13 align=center><b><font face="msyh">%s</font></b><br/><br/></para>' %(menge)
    menge_p = Paragraph(menge_para, normalStyle)
    gesamtbetrag = "Gesamtbetrag"
    gesamtbetrag_para = '<para autoLeading="off" fontsize=13 align=center><b><font face="msyh">%s</font></b><br/><br/></para>' %(gesamtbetrag)
    gesamtbetrag_p = Paragraph(gesamtbetrag_para, normalStyle)

    gesamtsv = "Gesamtbetrag Versand"
    gesamtsv_para = '<para autoLeading="off" fontsize=12 align=left><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(gesamtsv)
    gesamtsv_p = Paragraph(gesamtsv_para, normalStyle)
    gesamtwb = "Gesamtbetrag Werbeaktion"
    gesamtwb_para = '<para autoLeading="off" fontsize=12 align=left><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(gesamtwb)
    gesamtwb_p = Paragraph(gesamtwb_para, normalStyle)
    zwischensumme = "Zwischensumme"
    zwischensumme_para = '<para autoLeading="off" fontsize=12 align=left><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(zwischensumme)
    zwischensumme_p = Paragraph(zwischensumme_para, normalStyle)

    gesamtbetragall = "Gesamtbetrag"
    gesamtbetragall_para = '<para autoLeading="off" fontsize=12 align=left><br/><b><font face="msyh">%s</font></b><br/><br/></para>' %(gesamtbetragall)
    gesamtbetragall_p = Paragraph(gesamtbetragall_para, normalStyle)

    default = getPValue(" ")
    bis0_dingdanhao = [default]
    bis0_pro = [default]
    bis0_menge = [default]
    bis0_gesa = [default]
    bis1_dingdanhao = [default]
    bis1_pro = [default]
    bis1_menge = [default]
    bis1_gesa = [default]
    bis2_dingdanhao = [default]
    bis2_pro = [default]
    bis2_menge = [default]
    bis2_gesa = [default]
    yunprices_in = [default]
    guanggaoprices_in = [default]
    if len(bmenge_values) >= 1:
        bis0_dingdanhao = [getPValue(dingdanhao)]
        bis0_pro = [getPValue(aclass_values[0])]
        bis0_menge = [getPValue(bmenge_values[0])]
        bis0_gesa = [getPValue(gesamtbetrag_values[0])]
    if len(bmenge_values) >= 2:
        bis1_dingdanhao = [getPValue(dingdanhao)]
        bis1_pro = [getPValue(aclass_values[1])]
        bis1_menge = [getPValue(bmenge_values[1])]
        bis1_gesa = [getPValue(gesamtbetrag_values[1])]
    if len(bmenge_values) >= 3:
        bis2_dingdanhao = [getPValue(dingdanhao)]
        bis2_pro = [getPValue(aclass_values[2])]
        bis2_menge = [getPValue(bmenge_values[2])]
        bis2_gesa = [getPValue(gesamtbetrag_values[2])]

    yunprices_count_in = [default]
    guanggaoprices_count_in = [default]
    if len(yunprices) > 0:
        yunprices_in = [getPValue(yunprices[0])]
        yunprices_count_in = [getPValue(str(biscount))]
    if len(guanggaoprices) > 0:
        guanggaoprices_in = [getPValue(guanggaoprices[0])]
        guanggaoprices_count_in = [getPValue(str(biscount))]

    component_data= [
        [[title_p], '', '', ''],
        [[rechnung_p], '', '', ''],
        [[to_p], '', [bestellnummer_p], ''],
        [[getPValue(address)], '', [getPValue(dingdanhao)], ''],
        ['', '', [getPValue(time)], ''],
        [[bestellnr_p], [produktdetails_p], [menge_p], [gesamtbetrag_p]],
        [bis0_dingdanhao, bis0_pro, bis0_menge, bis0_gesa],
        [bis1_dingdanhao, bis1_pro, bis1_menge, bis1_gesa],
        [bis2_dingdanhao, bis2_pro, bis2_menge, bis2_gesa],
        [[gesamtsv_p], '', yunprices_count_in, yunprices_in],
        [[gesamtwb_p], '', guanggaoprices_count_in, guanggaoprices_in],
        [[zwischensumme_p], '', [getPValue(str(biscount))], [getPValue(totalprice_value)]],
        [[gesamtbetragall_p], '', [getPValue(str(biscount))], [getPValue(totalprice_value)]],
    ]

    # 创建表格对象，并设定各列宽度
    component_table = Table(component_data, colWidths = [160, 200, 80, 120])

    #添加表格样式
    component_table.setStyle(TableStyle([
    ('SPAN',(0,0),(3,0)), # 合并第1行
    ('SPAN',(0,1),(3,1)), # 合并第2行
    ('SPAN',(0,2),(1,2)), # 合并第3行
    ('SPAN',(2,2),(3,2)), # 合并第3行
    ('SPAN',(0,3),(1,4)), # 合并第4,5行
    ('SPAN',(2,3),(3,3)), # 合并第4行
    ('SPAN',(2,4),(3,4)), # 合并第5行
    ('SPAN',(0,9),(1,9)), # 合并第10行
    ('SPAN',(0,10),(1,10)), # 合并第11行
    ('SPAN',(0,11),(1,11)), # 合并第12行
    ('SPAN',(0,12),(1,12)), # 合并第13行
    ('BACKGROUND',(0,0),(-1,0), colors.lightsalmon), # 设置第1行背景颜色
    ('BACKGROUND',(0,1),(-1,1), colors.lightsalmon), # 设置第2行背景颜色 lightcoral
    ('BACKGROUND',(0,2),(-1,2), colors.lightgrey), # 设置第3行背景颜色
    ('BACKGROUND',(0,5),(-1,5), colors.lightgrey), # 设置第3行背景颜色
    ('FONTNAME', (0,0), (-1,-1), 'msyh'), # 字体
    # ('FONTSIZE', (0,0), (-1,-1), 10), # 字体大小
    ('FONTSIZE', (0,0), (-1,0), 25), # 字体大小
    ('ALIGN',(0, 0),(-1,-1), 'LEFT'),# 对齐
    ('VALIGN',(-1,0),(-2,0), 'MIDDLE'),  # 对齐
    ('LINEBEFORE',(0,0),(0,-1), 0.1, colors.grey), #设置表格左边线颜色为灰色，线宽为0.1
    ('TEXTCOLOR', (0,0), (-1,-1), colors.royalblue), # 设置表格内文字颜色
    ('GRID', (0,0), (-1,-1), 0.8, colors.black), # 设置表格框线为红色，线宽为0.5
    ]))
    story.append(component_table)

    doc = SimpleDocTemplate(pdfoutpath)
    doc.build(story)

# ================================ 处理文件 ================================
def handleFile(filePath):
    file_object = open(filePath)
    try:
        all_the_text = file_object.read()
    finally:
         file_object.close()

    # 过滤掉无效文件
    if filePath.find(".html") < 0:
        print "====================无需处理===================="
        text.insert(END, '====================无需处理====================\n')
        text.insert(END, '无需处理:' + filePath + '\n')
        text.see(END)
        return

    print "====================分析文件===================="
    text.insert(END, '====================分析文件====================\n')
    text.see(END)

    # 找订单号
    span_value = r'<span.*?>(.*?)</span>'
    # dingdanhao_value = r'<span class="a-size-medium a-text-bold" .*?>(.*?)</span>'
    # dingdanhao_values = re.findall(span_value, all_the_text, re.S|re.M)
    # for item in dingdanhao_values:
    #     if item.find("Bestellnr.: #") == 0:
    #         start = len("Bestellnr.: #")
    #         end = len(item)
    #         dingdanhao = item[start + 1:end]
    ddhStart = all_the_text.find("Bestellnr.: # ") + len("Bestellnr.: # ")
    dingdanhao = all_the_text[ddhStart : ddhStart + 19]

    # print dingdanhao_values
    # 找表格
    biaoge_value = r'<table .*?>(.*?)</table>'
    biaoge_values = re.findall(biaoge_value, all_the_text, re.S|re.M)
    # print "共有表格数量：" , len(biaoge_values)
    # print "tr:", biaoge_values[0]
    # 取第1个表格
    usebiaoge1 = biaoge_values[0]
    tr_value = r'<tr>(.*?)</tr>'
    th_value = r'<th.*?>(.*?)</th>'
    td_value = r'<td.*?>(.*?)</td>'
    tr_values = re.findall(tr_value, usebiaoge1, re.S|re.M)
    # print "tr:", tr_values

    have_Lieferung_bis = usebiaoge1.find('Lieferung bis') >= 0
    for i in range(0, len(tr_values)):
        tr = tr_values[i]
        th_values = re.findall(th_value, tr, re.S | re.M)
        for th in th_values:
            if th.find("span") >= 0:
                hangmings = re.findall(span_value, th, re.S | re.M)
                hanming = hangmings[0]
            else:
                hanming = th;
            # print "行名:" + hanming
        td_values = re.findall(td_value, tr, re.S | re.M)
        # print "td:", td_values
        for td in td_values:
            if '<br>' in td:
                td = td.replace('    ', '')  # 过滤该标签
                td = td.replace('\n', '')  # 换行空格替代 否则总换行
            td = td.replace('<span class="a-letter-space"></span>', " ");
            if td.find("<span ") >= 0:
                hangzhis = re.findall(span_value, td, re.S | re.M)
                # print "行值中:", hangzhis
                hangzhi = hangzhis[0]
            else:
                hangzhi = td
            # print "行值:", hangzhi
            # 处理<br>
            if '<br>' in hangzhi:
                hangzhi = hangzhi.replace('\n', '')
                hangzhi = hangzhi.replace('<br>', '<br/>')
            # print "hangzhi:", hangzhi
        if have_Lieferung_bis:
            if 3 == i:
                address = hangzhi;
            elif 4 == i:
                end = hangzhi.rfind(',')
                time = "Kaufdatum " + hangzhi[0 : end];
        else:
            if 2 == i:
                address = hangzhi;
            elif 3 == i:
                end = hangzhi.rfind(',')
                time = "Kaufdatum " + hangzhi[0 : end];

    # 取第2个表格
    # usebiaoge2 = biaoge_values[1]
    # 获取Produktdetails 单个商品描述
    aclass_value = r'<a class="a-link-normal a-text-bold".*?>(.*?)</a>'
    aclass_values = re.findall(aclass_value, all_the_text, re.S|re.M)

    # 获取Bestellte Menge 单个商品下单个数
    bmenge_value = r'<td id="myo-order-details-item-quantity-ordered" class="a-size-medium a-text-right a-text-bold">(.*?)</td>'
    bmenge_values = re.findall(bmenge_value, all_the_text, re.S|re.M)

    # 获取Versandte Menge 单个商品发货个数
    menge_value = r'<td id="myo-order-details-item-quantity-shipped" class="a-size-medium a-text-right a-text-bold">(.*?)</td>'
    menge_values = re.findall(menge_value, all_the_text, re.S|re.M)

    # 获取Gesamtbetrag，单个商品的单价
    gesamtbetrag_value = r'<span id="myo-order-details-item-sub-total">(.*?)</span>'
    gesamtbetrag_values = re.findall(gesamtbetrag_value, all_the_text, re.S|re.M)

    # 获取Gesamtbetrag Artikel，单个商品的总价
    gesamtbetrag_aritikel_value = r'<span id="myo-order-details-item-total" class="a-text-bold">(.*?)</span>'
    gesamtbetrag_aritikel_values = re.findall(gesamtbetrag_aritikel_value, all_the_text, re.S|re.M)
    #
    # # 获取，单个商品运费
    # gesamtbetrag_versand = r'<span id="myo-order-details-order-shipping-total">(.*?)</span>'
    # gesamtbetrag_versands = re.findall(gesamtbetrag_versand, all_the_text, re.S|re.M)

    # 获取全部的运费总价
    yunprice = r'<span id="myo-order-details-order-shipping-total">(.*?)</span>'
    yunprices = re.findall(yunprice, all_the_text, re.S|re.M)
    # 获取全部的广告费总价
    guanggaoprice = r'<span id="myo-order-details-order-promotion-total">(.*?)</span>'
    guanggaoprices = re.findall(guanggaoprice, all_the_text, re.S|re.M)

    # 获取全部的总价
    totalprice = r'<a id="myo-order-details-order-grand-total".*?>(.*?)</a>'
    totalprices = re.findall(totalprice, all_the_text, re.S|re.M)
    print "totalprices size: ", len(totalprices)
    if len(totalprices) <= 0:
        totalprice = r'<span id="myo-order-details-order-grand-total".*?>(.*?)</span>'
        totalprices = re.findall(totalprice, all_the_text, re.S | re.M)
    totalprice_value = totalprices[0]

    # 数据预处理及判定
    address = address.replace("   ", " ")
    # 商品总个数
    biscount = 0;
    for menge in bmenge_values:
        menge = menge.replace(' ', "");
        biscount += int(menge);

    # 价格总计
    pricesum = 0;
    for price in gesamtbetrag_aritikel_values:
        print "price:", price
        price = price.replace('&nbsp;', "")
        price = price.replace('\xc2\xa0', "")
        price = price.replace('€', "")
        price = price.replace(',', ".")
        print "price:", price
        pricesum += float(price)
    pricesumvalue = str(pricesum) + " €"
    pricesumvalue = pricesumvalue.replace('.', ',')

    print "====================输出结果===================="
    text.insert(END, '====================输出结果====================\n')
    text.see(END)
    print dingdanhao
    print time
    print address
    if len(bmenge_values) >= 1:
        print aclass_values[0]
        print bmenge_values[0]
        print gesamtbetrag_aritikel_values[0]
        # print gesamtbetrag_versands[0]
    if len(bmenge_values) >= 2:
        print aclass_values[1]
        print bmenge_values[1]
        print gesamtbetrag_aritikel_values[1]
        # print gesamtbetrag_versands[1]
    if len(bmenge_values) >= 3:
        print aclass_values[2]
        print bmenge_values[2]
        print gesamtbetrag_aritikel_values[2]
        # print gesamtbetrag_versands[2]

    # 生成成功
    pdfoutpath = path_to_watch + '\\Rechnung(' + dingdanhao + ').pdf'
    outPDF(pdfoutpath,
           dingdanhao,
           time,
           address,
           aclass_values,
           bmenge_values,
           gesamtbetrag_values,
           gesamtbetrag_aritikel_values,
           biscount,
           yunprices,
           guanggaoprices,
           totalprice_value)

    print "====================生成成功===================="
    text.insert(END, '====================生成成功====================\n')
    text.insert(END, '生成:' + pdfoutpath + '\n')
    text.see(END)

# ================== 监听文件 ==================
def wathingFile2():
    print "====================扫描文件===================="
    text.insert(END, '====================扫描文件====================\n')
    text.see(END)
    ACTIONS = {
        1: "Created",
        2: "Deleted",
        3: "Updated",
        4: "Renamed from something",
        5: "Renamed to something"
    }

    FILE_LIST_DIRECTORY = 0x0001

    print 'Watching changes in', path_to_watch
    hDir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while 1:
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            # win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES,
            win32con.FILE_NOTIFY_CHANGE_SIZE,
            # win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            # win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None)
        time.sleep(2)
        for action, filename in results:
            full_filename = os.path.join(path_to_watch, filename)
            ac = ACTIONS.get(action, "Unknown")
            print full_filename, ac
            if ac == "Updated":
                # handleFile(full_filename)
                try:
                    handleFile(full_filename)
                except Exception, e:
                    print e
                    text.insert(END, '错误：' + str(e) + '\n')
                    text.see(END)
            elif ac == "Deleted":
                print "已删除文件: ", full_filename
                text.insert(END, '已删除文件:' + full_filename + '\n')
                text.see(END)

        print "====================继续扫描===================="
        text.insert(END, '====================继续扫描====================\n')
        text.see(END)
# ================== 扫描文件 ==================
def wathingFile1():
    print "====================扫描文件===================="
    text.insert(END, '====================扫描文件====================\n')
    text.see(END)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    before = dict ([(f, None) for f in os.listdir (path_to_watch)]) ##使用dict，不使用list
    while 1:
        time.sleep(3)
        print time.strftime(ISOTIMEFORMAT, time.localtime()) + ' 自动扫描一次文件...\n'
        text.insert(END, time.strftime(ISOTIMEFORMAT, time.localtime()) + ' 自动扫描一次文件...\n')
        text.see(END)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]  ##这也是为什么使用dict，而不直接使用list的原因
        removed = [f for f in before if not f in after]
        if added:
            for addedFilename in added:
                filepath = path_to_watch + "\\" + addedFilename;
                print "添加文件: ", filepath
                text.insert(END, '添加文件:' + addedFilename + '\n')
                text.see(END)

                # handleFile(filepath)
                try:
                    handleFile(filepath)
                except Exception, e:
                    print e
                    text.insert(END, '错误：' + str(e) + '\n')
                    text.see(END)
                finally:
                    print "====================继续扫描===================="
                    text.insert(END, '====================继续扫描====================\n')
                    text.see(END)

        if removed:
            for removedFilename in removed:
                print "已删除文件: ", removedFilename
                text.insert(END, '已删除文件:' + removedFilename + '\n')
                text.see(END)
        before = after

# ================== 主界面 ==================
# root = Tk()
# root.title("坏家伙")
#
# def callback():
#
# Button(root, text = "开始扫描", fg = "blue", bd = 2, width = 20, height = 5, command = callback).pack()
# root.mainloop()

# Button(root, text="外观装饰边界附近的标签", width=19,relief=GROOVE,bg="red").pack()
# Button(root, text="设置按钮状态",width=21,state=DISABLED).pack()
# Button(root, text="设置bitmap放到按钮左边位置", compound="left",bitmap="error").pack()
# Button(root, text ="设置高度宽度以及文字显示位置",anchor = 'sw',width = 30,height = 2).pack()

def count(i):
    global WORKING
    if WORKING:
        print "====================已在扫描===================="
        text.insert(END, '====================已在扫描====================\n')
        text.see(END)
        return;

    if True:
        try:
            WORKING = True
            wathingFile2();
            WORKING = False
        except Exception, e:
            print e
            text.insert(END, '扫描错误：' + str(e) + '\n')
            text.see(END)
        finally:
            print "====================结束扫描===================="
            text.insert(END, '====================结束扫描====================\n')
            text.see(END)
    else:
        WORKING = True
        wathingFile2();
        WORKING = False
        print "====================结束扫描===================="
        text.insert(END, '====================结束扫描====================\n')
        text.see(END)

    buttonWrok.setvar()

def fun():
    text.insert(END, '开始扫描...\n')
    varTips.set('提示：扫描中......')
    th = threading.Thread(target=count, args=(0,))
    th.setDaemon(True)  # 守护线程
    th.start()

def handleclear():
    # 删除工作目录下的非文件夹文件
    for root, dirs, files in os.walk(path_to_watch):
        print root
        print dirs
        print files
        for name in files:
            os.remove(os.path.join(root, name))
            print("已删除文件: " + os.path.join(root, name))
            text.insert(END, "已删除文件: " + os.path.join(root, name) + '\n')
            text.see(END)

def clear():
    ok = tkMessageBox.askokcancel("确定", "清空工作目录全部文件？")
    if ok:
        print "clear"
        handleclear()

def openworkingdir():
    os.system("explorer.exe %s" % path_to_watch)

root = Tk()
root.title('YL-tiger')
# 窗口呈现位置
root.geometry('+50+50')
varDir = StringVar()  # 设置变量
labelDir = Label(root, font=('微软雅黑', 10), fg='black', justify = 'left', textvariable=varDir)
labelDir.grid(row = 0, column = 0)
buttonWorkingDir = Button(root, text='打开工作目录', font=('微软雅黑', 10), fg='black', command=openworkingdir)
buttonWorkingDir.grid(row = 0, column = 1)
buttonClear = Button(root, text='清空工作目录文件', font=('微软雅黑', 10), fg='red', command=clear)
buttonClear.grid(row = 0, column = 2)
varDir.set('工作目录： ' + path_to_watch)
text = ScrolledText(root, font=('微软雅黑', 10), fg='blue')
text.grid(row = 1, column = 0, columnspan = 3)
buttonWrok = Button(root, text='开始扫描', font=('微软雅黑', 10), command=fun)
buttonWrok.grid(row = 2, column = 1)
varTips = StringVar()  # 设置变量
label = Label(root, font=('微软雅黑', 10), fg='red', textvariable=varTips)
label.grid(row = 2, column = 0)
varTips.set('提示：请点击开始扫描!')
root.mainloop()
