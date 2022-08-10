# spider-project

### 大唐集团公司:
http://www.cdt-ec.com，
 
run: four.py

### taobao
login
https://login.taobao.com/member/login.jhtml
run: 1688 1688search 

#### 相关文档

1.run.sh 启动chrome的remote debugger模式
2.debug.py 连接chrome的debugger，这样解决了自动登陆的问题
run:1688.py 1688search.py

###  中船重工电子采购平台
url="http://www.ebuy.csemc.com"
 
run: center.py

### 国家电投
https://ebid.espic.com.cn
 
run: ebid.py

### 国能E购
https://www.neep.shop/

run:neep

### 华电
https://www.chdtp.com

run:dian

> 使用 batch.sh 批量执行

#### how to

> use tools.py to create batch.sh file,then run batch.sh file to get result

### 华能
http://ec.chng.com.cn/ecmall/

run:neng.py

### 目录命名规则

国家电投: 采购需求单位+采购单名称+采购单编号。
国能e购\查询日期(20220723)\截止日期+项目名称+采购编号\采购编号.html(如果有附件，则使用系统命名的 附件名称)
华电:  截止日期+采购单位+采购标题+采购单号；
华能:  询价单位+采购方案名称；


### 有待解决的问题
* neng 的记录数取的不对


### error

requests.exceptions.SSLError: HTTPSConnectionPool(host='www.chdtp.com', port=443): Max retries exceeded with url: /zbcg/cggl/displaysCgbjAction.action (Caused by SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:997)')))


### 字符集问题

> <meta http-equiv="Content-Type" content="text/html;charset=gb2312">

### 中船搜索 水位计 错误
