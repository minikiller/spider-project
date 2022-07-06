# -*- coding: utf-8 -*-
import pandas as pd

### 返回索引数组

def getIndex():

    df = pd.read_excel('index.xlsx')

    # print(df)   
    data=[]
    # Iterate over column names 
    for column in df: 
        
        # Select column contents by column 
        # name using [] operator 
        columnSeriesObj = df[column] 
        # print('Colunm Name : ', column)
        data.append(column) 
        # print('Column Contents : ', columnSeriesObj.values) 
        for value in columnSeriesObj.values:
            data.append(value) 
    print(data)
    return data

# str中的字符串是否包含中strList数组中
def indexOfStr(str,strList):
    """
    str字符串是否包含strList数组中的字符串
    
    :param str: this is a first param
    :param strList: this is a second param
    :returns: True or False
    """

    # data=[x in str for x in strList]
    result=any(x in str for x in strList)
    return result

if __name__ == '__main__':
    data=getIndex()
    result=indexOfStr("水位sdfd",data)
    print(result)

