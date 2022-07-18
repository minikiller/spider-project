import re
string="自主订阅 (15)"
dsd=re.findall(r"\d+\.?\d*",string)
print(int(dsd[0])//10)

 
