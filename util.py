def getPage(totalPage,pageSize):
    data=totalPage//pageSize
    if (totalPage%pageSize)>0:
        data=data+1
    return range(1,data+1)

def getNumber(str):
    import re
    num=re.findall(r"\d+\.?\d*",str)
    return num[0]

def get_cookies(browser):
    cookies = {}
    selenium_cookies = browser.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies