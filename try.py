totalPage=305
pageSize=50

data=totalPage//pageSize
if (totalPage%pageSize)>0:
    data=data+1
for i in range(1,data+1):
    print(i)