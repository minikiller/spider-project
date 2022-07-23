from datetime import datetime, timedelta

import logging


def getPage(totalPage, pageSize):
    data = totalPage//pageSize
    if (totalPage % pageSize) > 0:
        data = data+1
    return range(1, data+1)


def getNumber(str):
    import re
    num = re.findall(r"\d+\.?\d*", str)
    return num[0]


def get_cookies(browser):
    cookies = {}
    selenium_cookies = browser.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

# 在指定文件中替换指定内容


def replaceFile(filename, source, target):

    # read input file
    with open(filename, "rt") as fin:
        # read file contents to string
        data = fin.read()
        # replace all occurrences of the required string
        data = data.replace(source, target)

    # open the input file in write mode
    with open(filename, "wt") as fin:
        # overrite the input file with the resulting data
        fin.write(data)


def downloadFile(url, filename):
    import requests
    r = requests.get(url, allow_redirects=True)
    try:
        with open(filename, 'wb') as f:
            f.write(r.content)
        logging.info(f"{filename} 下载成功")
    except Exception as e:
        logging.error(f"{filename} 下载失败,错误是: {e}")

# 如果超过指定时间，则返回当前日期，否则返回提前一天的日期

def compDate(_date):
    tmpDate = _date[:10]+" 09:00:00"
    sourceDate = datetime.strptime(_date, "%Y-%m-%d %H:%M:%S")
    targetDate = datetime.strptime(tmpDate, "%Y-%m-%d %H:%M:%S")
    print(sourceDate, targetDate)
    if sourceDate > targetDate:
        return _date[:10]
    else:
        return (sourceDate + timedelta(days=-1)).strftime("%Y-%m-%d")


if __name__ == '__main__':
    # replaceFile("./20220719/6HRNR020220700298.html")
    re = compDate("2022-07-26 09:19:53")
    print(re)
