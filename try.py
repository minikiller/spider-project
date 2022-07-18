# totalPage=305
# pageSize=50

# data=totalPage//pageSize
# if (totalPage%pageSize)>0:
#     data=data+1
# for i in range(1,data+1):
#     print(i)
# import requests

# myurl="https://b2b.crpower.com.cn/ispweb/pcux5PonHeaders/searchWinningList.do"
# request_body= {"data":
#                 '{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate":"2022-07-16", "endDate":"2022-07-18"}',
#                 "take": 20,
#                 "skip": 0,
#                 "page": 1,
#                 "pageSize": 20}
# from fake_useragent import UserAgent
# user_agent = UserAgent(verify_ssl=False).random
# headers = {"User-Agent": user_agent,'Content-Type': 'application/x-www-form-urlencoded'}
# response = requests.post(myurl, data=request_body,headers=headers)
# print(response.json())

import html
import json
endDate = html.getToDate()
startDate = html.getYesDate()
print(endDate)
print(startDate)
query = {"sourceMethods": "公开",
         "sourceStatus": "ACTIVE",
         "queryAll": "",
         "sourceTypeTag": "WZ",
         "startDate":  startDate,
         "endDate": endDate}

str = json.dumps(query)

# query='{"sourceMethods":"公开", "sourceStatus":"ACTIVE", "queryAll":"", "sourceTypeTag":"WZ","startDate":'+ startDate+', "endDate":'+'endDate'

print(str)
