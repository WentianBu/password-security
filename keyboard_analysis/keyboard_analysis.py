#coding=utf-8
#键盘分析
#（1）分别读取csdn和yahoo数据库中的passwd
#（2）自定义了常见的14种键盘密码字符串
#（3）将从数据库中读取的passwd与定义的字符串进行子串匹配（忽略单个的字母和数字）
#（4）只选择相对高频的密码，生成保存频率最高的密码和对应频率的csv
import pandas as pd
import numpy as np
import csv
np.set_printoptions(suppress=True)

##############################################
#（1）读取数据
##############################################
yahoo_data = pd.read_csv('Yahoo-original-mail-passwd.csv',engine='python',sep='\t', quoting=csv.QUOTE_NONE,names=["email","passwd"], quotechar='"', error_bad_lines=False)
csdn_data = pd.read_csv('csdn-original-username-mail-passwd.csv',engine='python',sep='\t', quoting=csv.QUOTE_NONE,names=["name","email","passwd"],quotechar='"', error_bad_lines=False)

#读取密码
yahoo_passwd = pd.Series(yahoo_data['passwd'].values)
csdn_passwd = pd.Series(csdn_data['passwd'].values)

##############################################
#（2）定义常见的键盘密码字符串
##############################################
keyboard_pass1 = '1234567890qwertyuiopasdfghjkl;zxcvbnm,./'
keyboard_pass2 = '1234567890poiuytrewqasdfghjkl;/.,mnbvcxz'
keyboard_pass3 = '1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,9ol.0p;/'
keyboard_pass4 = '1qazxsw23edcvfr45tgbnhy67ujm,ki89ol./;p0'
keyboard_pass5 = 'zaq1xsw2cde3vfr4bgt5nhy6mju7,ki8.lo9/;p0'
keyboard_pass6 = 'zaq12wsxcde34rfvbgt56yhnmju78ik,.lo90p;/'
keyboard_pass7 = '0987654321poiuytrewq;lkjhgfdsa/.,mnbvcxz'
keyboard_pass8 = '0987654321qwertyuioplkjhgfdsazxcvbnm,./'
#忽略数字行
keyboard_pass9 = 'qazwsxedcrfvtgbyhnujmik,ol.p;/'
keyboard_pass10 = 'qazxswedcvfrtgbnhyujm,kiol./;p'
keyboard_pass11 = 'zaqxswcdevfrbgtnhymju,ki.lo/;p'
keyboard_pass12 = 'zaqwsxcderfvbgtyhnmjuik,.lop;/'
keyboard_pass13 = 'pl,okmijnuhbygvtfcrdxeszwaq'
keyboard_pass14 = 'pl,mkoijnbhuygvcftrdxzsewaq'

keyboard_pass_all = keyboard_pass1 + keyboard_pass2 + keyboard_pass3 + keyboard_pass4 + keyboard_pass5 + keyboard_pass6 + keyboard_pass7 + keyboard_pass8 + keyboard_pass9 + keyboard_pass10 + keyboard_pass11+keyboard_pass12+keyboard_pass13+keyboard_pass14

##############################################
#（3）分别在两个数据集中进行密码的子串匹配
##############################################
#定义字典来保存密码和其出现次数
yahoo_output = dict()
csdn_output = dict()
#######################YAHOO数据集
y_sum = 0
for data in yahoo_passwd.values:
	data = str(data)#格式都转换为string类型
	# 密码是定义的键盘密码字符串的子串并且不是单个的字母或数字
	if data in keyboard_pass_all and len(data) > 1:
		y_sum = y_sum + 1
		if yahoo_output.has_key(data):
			#密码已经存在，出现次数加一
			yahoo_output[data] = yahoo_output[data]+ 1
		else:#否则，出现次数为1
			yahoo_output[data] = 1
#######################CSDN数据集
c_sum = 0
for data in csdn_passwd.values:
	data = str(data)
	if data in keyboard_pass_all and len(data) > 1:
		c_sum = c_sum + 1
		if csdn_output.has_key(data):
			csdn_output[data] = csdn_output[data] + 1
		else:
			csdn_output[data] = 1

###############################################################
#（4）计算频率，选择相对高频的密码，并生成排名结果csv文件
###############################################################
#######################YAHOO数据集
#去掉出现次数少于 10 次的低频密码
result = dict()
for data in yahoo_output:
	if yahoo_output[data] >= 10:
		result[data] = yahoo_output[data]
yahoo_output = result
yahoo_output = pd.Series(yahoo_output)
#降序排序
yahoo_output = yahoo_output.sort_values(ascending = False)
yahoo = pd.DataFrame({'password' : yahoo_output.index , 'numbers' : yahoo_output.values , 'probability' : None})
#计算频率
index_yahoo = yahoo.index
for index in index_yahoo:
	yahoo.loc[index , 'probability'] =  str(float(yahoo.loc[index , 'numbers']) / y_sum).format(':.8f')
#生成排序后的csv结果文件
yahoo.to_csv('result_yahoo.csv' , columns = ['password' , 'numbers' , 'probability'])
#######################CSDN数据集
#去掉出现次数少于 20 次的低频密码
result.clear()
for data in csdn_output:
	if csdn_output[data] >= 20:
		result[data] = csdn_output[data]
csdn_output = result
csdn_output = pd.Series(csdn_output)
csdn_output = csdn_output.sort_values(ascending = False)
csdn = pd.DataFrame({'password' : csdn_output.index , 'numbers' : csdn_output.values , 'probability' : None})
index_csdn = csdn.index
for index in index_csdn:
	csdn.loc[index , 'probability'] =  str(float(csdn.loc[index , 'numbers']) / c_sum).format(':.8f')
#生成排序后的csv结果文件
csdn.to_csv('result_csdn.csv' , columns = ['password' , 'numbers' , 'probability'])