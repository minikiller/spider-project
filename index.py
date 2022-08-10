# -*- coding: utf-8 -*-
import pandas as pd
import logging

### 返回关键字索引数组

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
    logging.debug(f"查询关键字: {data}")
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
    result = indexOfStr("分谈-703所-无锡分部-锅炉汽包水位计", data)
    print(result)

