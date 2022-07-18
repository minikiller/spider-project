# -*- coding: utf-8 -*-
from lxml import etree
import time
import os

# from lxml import html


def exportHtml(str, fileName):
    str1 = str.splitlines()  # remove /r/n
    # open file in write mode
    with open(fileName, 'w', encoding='utf-8') as fp:
        for item in str1:
            # write each item on a new line
            fp.write("%s\n" % item)
        # print(f'finish write to {fileName}, Done')


def exportTempHtml(str, fileName):
    try:
        os.mkdir("./tmp")
    except OSError as error:
        print(error)
    str1 = str.splitlines()  # remove /r/n
    fileName = "./tmp/"+fileName
    # open file in write mode
    with open(fileName, 'w', encoding='utf-8') as fp:
        for item in str1:
            # write each item on a new line
            fp.write("%s\n" % item)


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
    path = '//*[@id="gform"]/div[1]/div[3]/div/table/tbody/tr'
    href = tree.xpath("/html/body/div/div/table/tr/td[2]")
    # /html/body/div/div/table/tbody/tr[1]/td[2]
    # for value in href:
    #     # print(value.text)
    #     index.getIndex
    return href


def outResultData(fileName):
    logfile = "./logger.txt"
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


def getYesDate():
    from datetime import datetime, date, timedelta
    yesterday = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
    return yesterday


def getToDate():
    date_str = time.strftime("%Y-%m-%d", time.localtime())
    return date_str


def getResultData1(fileName):
    # import index
    with open(fileName, "r") as f:
        page = f.read()
    # tree = html.parse(r'./sales.html')
    # print(page)
    tree = etree.HTML(page)
    # # print(tree)
    # path='/html/body/div'
    path = '/html/body/div[2]/form/div[1]/div[3]/div/table/tr/td[2]'
    href = tree.xpath(path)
    # /html/body/div/div/table/tbody/tr[1]/td[2]
    # for value in href:
    #     # print(value.text)
    #     index.getIndex
    return href


if __name__ == '__main__':
    # date_str=getCurDate()
    # print(date_str)
    data = getResultData1("./tmp/XJ022071800929.html")
    print(len(data))
