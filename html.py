# -*- coding: utf-8 -*-
from lxml import etree
import time,os

# from lxml import html

def exportHtml(str,fileName):
    str1=str.splitlines() # remove /r/n 
    # open file in write mode
    with open(fileName, 'w') as fp:
        for item in str1:
            # write each item on a new line
            fp.write("%s\n" % item)
        print(f'finish write to {fileName}, Done')

def getResultContent(content):
    tree = etree.HTML(content)
    # print(tree) 
    href = tree.xpath("/html/body/div/div/table/tr/td[2]")
    # /html/body/div/div/table/tbody/tr[1]/td[2]
    # for value in href:
    #     # print(value.text)
    #     index.getIndex
    return href

def getResultData(fileName):
    # import index
    with open(fileName, "r") as f:
        page = f.read()
    # tree = html.parse(r'./sales.html')
    tree = etree.HTML(page)
    # print(tree) 
    href = tree.xpath("/html/body/div/div/table/tr/td[2]")
    # /html/body/div/div/table/tbody/tr[1]/td[2]
    # for value in href:
    #     # print(value.text)
    #     index.getIndex
    return href

def outResultData(fileName):
    logfile="./logger.txt"
    with open(logfile, 'a') as fp:
        date_str = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        fp.write(date_str+" %s\n" % fileName)

def getCurDate():
    date_str = time.strftime('%Y%m%d', time.localtime())
    # date_str = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
    # print(date_str)
    try:
        os.mkdir(date_str)
    except OSError as error:
        print(error) 
    return date_str

if __name__ == '__main__':
    # date_str=getCurDate()
    # print(date_str)
    getResultData("./20220705/2a974f9f7e1242fea8881313209a6bb7.html")

