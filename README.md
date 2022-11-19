# PyInvest

## Installation
```bash
# update python pip
python -m pip install -U pip
# clone latest repo
git clone https://github.com/crj1998/PyInvest.git
cd PyInvest
# install dependency package 
pip install -r requirements.txt
```
## Build
### Code Style check
```
python -m pylint --rcfile .pylintrc pyinvest
```
### Unit Test
```bash
python -m pytest
python -m pytest test/test_setup.py::TestSetup::test_version -v -s
```
## Develop
### ide.csdn
```bash
# Configure the pip source
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Upgrade pip
python -m pip install -U pip
mkdir /ide/workspace/lib
# install dependency package 
pip install -r requirements.txt -t /ide/workspace/lib --force-reinstall
export PYTHONPATH=$PYTHONPATH:/ide/workspace/lib
```
### eastmonet f-field
```
f2:最新价
f3:涨跌幅
f4:涨跌额
f5:总手（VOL）/成交量
f6:成交额
f7:振幅
f8:换手率
f9:市盈率(动态)
f10:量比
f11:5分钟涨跌幅
f12:股票代码
f13:市场
f14:股票名称
f15:今日最高
f16:今日最低
f17:今开
f18:昨收
f20:总市值
f21:流通市值
f22:涨速
f23:市净率
f24:60日涨跌幅
f25:年初至今涨跌幅
f26:上市时间
f28:昨日结算价
f30:每天最后一笔交易的成交量
f31:现汇买入价
f32:现汇卖出价
f33:委比
f34:外盘
f35:内盘
f37:净资产收益率加权（AOE）最近季度
f38:总股本
f39:流通A股（万股）
f40:总营收（最近季度）
f41:总营收同比（最近季度）
f44:总利润（最近季度）
f45:净利润（最近季度）
f46:净利润增长率（%）（同比）（最近季度）
f48:每股未分配利润
f49:毛利率（最近季度）
f50:总资产（最近季度）
f55+f56=f54
f57:负债率
f58:股东权益
f62:今日主力净流入
f64：超大单流入
f65:超大单流出
f66:今日超大单净流入
f69:超大单净比
f70:大单流入
f71:大单流出
f72:今日大单净流入
f75:大单净比
f76:中单流入
f77:中单流出
f78:今日中单净流入
f81:中单净比（%）
f82:小单流入
f83:小单流出
f84:进入小单净流入
f87:小单净比
f97:暂定
f98:暂定
f99:暂定
f100:行业
f102:地区板块
f103:备注
f104：上涨家数
f105:下跌家数
f106:平家家数
f112:每股收益（一）
f113:每股净资产
f114:市盈率（静）
f115:市盈率（TTM）
f124:交易时间
f128:板块领涨股
f129:净利润
f130:市销率TTM
f131:市现率TTM
f132:总营业收入TTM
f133:股息率
f134：行业板块的成分股数
f135:净资产
f138:净利润TTM
f164:5日主力净额
f166:5日超大单净额
f168:5日大单净额
f170:5日中单净额
f172:5日小单净额
f174:10日主力净额
f176:10日超大单净额
f178:10日大单净额
f180:10日中单净额
f182:10日小单净额
f348:可转债申购代码
f243：可转债申购日期
f350:涨停价
f351:跌停价
f352:均价
```