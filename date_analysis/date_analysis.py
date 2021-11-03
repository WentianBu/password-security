import sys

import configparser
import time
import re

import pandas as pd
from pandas import Series,DataFrame

#统计可能含日期的口令(连续数字位数大于等于4的)
def countProbPasswd(passwdList):
	df = []
	for i in range(len(passwdList)):
		passwd = str(passwdList[i])
		struc = ""
		for ch in passwd:
			if ch.isdigit():
				struc += 'D'
			elif ch.isalpha():
				struc += 'L'
			else:
				struc += 'S'

		char = struc[0]
		c = 1
		stri = struc[1:]
		res = ''
		for j in stri:
			if j == char:
				c += 1
			else:
				res += char
				res += str(c)
				char = j
				c = 1
		res += char
		res += str(c)

		#r'D[4-9]|D\d{2}'
		if re.search(r'D[4-9]|D\d{2}', res):
			df.append(passwd)
	return df

#统计含数字日期的口令-Yahoo
# 筛选出的符合条件的密码在 date_passwd/Yahoo 路径下
def analysisDate_Yahoo(data):
	lis1 = []
	lis2 = []
	lis3 = []
	lis4 = []
	lis5 = []
	lis6 = []
	lis7 = []
	lis8 = []
	lis9 = []
	datePasswd = {'yyyy':0,'yyyymm':0,'yyyymmdd':0,'mmddyyyy':0,'ddmmyyyy':0,'yymmdd':0,'mmddyy':0,'ddmmyy':0,'mmdd':0}
	for i in data:
		# 密码判断条件由长到短，符合多种条件的密码只归类于先进行判断的条件
		# 例如19800205，归类于yyyy-mm-dd而不是yyyy
		#yyyy-mm-dd
		if re.search(r'(19\d{2}|20\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['yyyymmdd'] += 1
			lis3.append(i)
			continue
		#mm-dd-yyyy
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(19\d{2}|20\d{2})',i):
			datePasswd['mmddyyyy'] += 1
			lis4.append(i)
			continue
		#dd-mm-yyyy
		if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])(19\d{2}|20\d{2})',i):
			datePasswd['ddmmyyyy'] += 1
			lis5.append(i)
			continue
		#yy-mm-dd
		if re.search(r'[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['yymmdd'] += 1
			lis6.append(i)
			continue
		#mm-dd-yy
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[0-9][0-9]',i):
			datePasswd['mmddyy'] += 1
			lis7.append(i)
			continue
		#dd-mm-yy
		if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])[0-9][0-9]',i):
			datePasswd['ddmmyy'] += 1
			lis8.append(i)
			continue
		#yyyy-mm
		if re.search(r'(19\d{2}|20\d{2})(0[1-9]|1[0-2])',i):
			datePasswd['yyyymm'] += 1
			lis2.append(i)
			continue
		#yyyy 1900-2100
		if re.search(r'19\d{2}|20\d{2}',i):
			datePasswd['yyyy'] += 1
			lis1.append(i)
			continue
		#mm-dd
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['mmdd'] += 1
			lis9.append(i)
			continue
	pd.Series(lis1).to_csv('date_passwd/Yahoo/yyyy.csv')
	pd.Series(lis2).to_csv('date_passwd/Yahoo/yyyymm.csv')
	pd.Series(lis3).to_csv('date_passwd/Yahoo/yyyymmdd.csv')
	pd.Series(lis4).to_csv('date_passwd/Yahoo/mmddyyyy.csv')
	pd.Series(lis5).to_csv('date_passwd/Yahoo/ddmmyyyy.csv')
	pd.Series(lis6).to_csv('date_passwd/Yahoo/yymmdd.csv')
	pd.Series(lis7).to_csv('date_passwd/Yahoo/mmddyy.csv')
	pd.Series(lis8).to_csv('date_passwd/Yahoo/ddmmyy.csv')
	pd.Series(lis9).to_csv('date_passwd/Yahoo/mmdd.csv')

	print('-------------Date passwd in Yahoo------------------')
	print(datePasswd)
	print('--------------------------------------------------')

#统计含数字日期的口令-csdn-密码
def analysisDate_csdn(data):
	lis1 = []
	lis2 = []
	lis3 = []
	lis4 = []
	lis5 = []
	lis6 = []
	lis7 = []
	lis8 = []
	lis9 = []
	datePasswd = {'yyyy':0,'yyyymm':0,'yyyymmdd':0,'mmddyyyy':0,'ddmmyyyy':0,'yymmdd':0,'mmddyy':0,'ddmmyy':0,'mmdd':0}
	for i in data:
		#yyyy-mm-dd
		if re.search(r'(19\d{2}|20\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['yyyymmdd'] += 1
			lis3.append(i)
			continue
		#mm-dd-yyyy
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(19\d{2}|20\d{2})',i):
			datePasswd['mmddyyyy'] += 1
			lis4.append(i)
			continue
		#dd-mm-yyyy
		if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])(19\d{2}|20\d{2})',i):
			datePasswd['ddmmyyyy'] += 1
			lis5.append(i)
			continue
		#yy-mm-dd
		if re.search(r'[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['yymmdd'] += 1
			lis6.append(i)
			continue
		#mm-dd-yy
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[0-9][0-9]',i):
			datePasswd['mmddyy'] += 1
			lis7.append(i)
			continue
		#dd-mm-yy
		if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])[0-9][0-9]',i):
			datePasswd['ddmmyy'] += 1
			lis8.append(i)
			continue
		#yyyy-mm
		if re.search(r'(19\d{2}|20\d{2})(0[1-9]|1[0-2])',i):
			datePasswd['yyyymm'] += 1
			lis2.append(i)
			continue
		#yyyy 1900-2100
		if re.search(r'19\d{2}|20\d{2}',i):
			datePasswd['yyyy'] += 1
			lis1.append(i)
			continue
		#mm-dd
		if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',i):
			datePasswd['mmdd'] += 1
			lis9.append(i)
			continue
	pd.Series(lis1).to_csv('date_passwd/csdn/yyyy.csv')
	pd.Series(lis2).to_csv('date_passwd/csdn/yyyymm.csv')
	pd.Series(lis3).to_csv('date_passwd/csdn/yyyymmdd.csv')
	pd.Series(lis4).to_csv('date_passwd/csdn/mmddyyyy.csv')
	pd.Series(lis5).to_csv('date_passwd/csdn/ddmmyyyy.csv')
	pd.Series(lis6).to_csv('date_passwd/csdn/yymmdd.csv')
	pd.Series(lis7).to_csv('date_passwd/csdn/mmddyy.csv')
	pd.Series(lis8).to_csv('date_passwd/csdn/ddmmyy.csv')
	pd.Series(lis9).to_csv('date_passwd/csdn/mmdd.csv')

	print('-------------Date passwd in CSDN------------------')
	print(datePasswd)
	print('--------------------------------------------------')

#含英文日期的口令-Yahoo
def analysisEnDate_Yahoo(data):
	dic = ['Jan','January','Feb','February','Mar','March','Apr','April',
			'May','Jun','June','Jul','July','Aug','August','Sep','September',
			'Oct','October','Nov','November','Dec','December']
	lis = []
	# 首先匹配日期字典dic里列出的那些
	# 如果字典中的月份缩写为某个人名或者单词的一部分，则忽略
	# 筛选规则（较为粗糙）：密码中出现字典列出的关键词时，如果关键词后一位是小写字母则丢弃
	for line in data:
		for i in dic:
			index = line.find(i)
			if index != -1:
				if index + len(i) == len(line):
					lis.append(str(line))
				elif not re.match(r'[a-z]', line[index + len(i)]):
					lis.append(str(line))
			# if i in str(line):
			# 	lis.append(str(line))
	pd.Series(lis).to_csv('date_passwd/Yahoo/en_date.csv')
	print('-------Passwords with English date in Yahoo-------')
	print(len(lis))
	print('--------------------------------------------------')

#含英文日期的口令-csdn
def analysisEnDate_csdn(data):
	dic = ['Jan','January','Feb','February','Mar','March','Apr','April',
			'May','Jun','June','Jul','July','Aug','August','Sep','September',
			'Oct','October','Nov','November','Dec','December']
	lis = []
	for line in data:
		for i in dic:
			index = line.find(i)
			if index != -1:
				if index + len(i) == len(line):
					lis.append(str(line))
				elif not re.match(r'[a-z]', line[index + len(i)]):
					lis.append(str(line))
			# if i in str(line):
			# 	lis.append(str(line))
	pd.Series(lis).to_csv('date_passwd/csdn/en_date.csv')
	print('-------Passwords with English date in CSDN-------')
	print(len(lis))
	print('--------------------------------------------------')

# 原有的英文日期分析，不准确
def analysisEnDate_old(data):
	dic = ['Jan','January','Feb','February','Mar','March','Apr','April',
			'May','Jun','June','Jul','July','Aug','August','Sep','September',
			'Oct','October','Nov','November','Dec','December']
	lis = []
	for line in data:
		for i in dic:
			if i in str(line):
				lis.append(str(line))
	pd.Series(lis).to_csv('date_passwd/en_date_old.csv')
	print(len(lis))
	print('--------------------------------------------------')

if __name__ == '__main__':

	time1 = time.perf_counter()
	#--------------------读文件模块--------------------#
	#读取passwd
	data_csdn = pd.read_csv('../DataSet/csdn-original-username-mail-passwd.csv', names=["name", "email", "passwd"], sep = '\t', engine='python', quoting=3, error_bad_lines=False)
	data_Yahoo = pd.read_csv('../DataSet/Yahoo-original-mail-passwd.csv', names=["email", "passwd"], sep = '\t', engine='python')
	passwdList_csdn = pd.Series(data_csdn['passwd'].values)
	passwdList_Yahoo = pd.Series(data_Yahoo['passwd'].values)
	#读口令结构文件
	time2 = time.perf_counter()
	print ('read file time : ' , (time2 - time1))

	#--------------------统计模块--------------------#
	lis_csdn = countProbPasswd(passwdList_csdn)
	lis_Yahoo = countProbPasswd(passwdList_Yahoo)

	#分析含日期的口令个数 打印
	analysisDate_csdn(lis_csdn)
	analysisDate_Yahoo(lis_Yahoo)

	#分析含英文日期的口令，原代码为analysisEnDate_old(lis)，会将例如Mary的人名截取出Mar当作日期
	analysisEnDate_csdn(lis_csdn)
	analysisEnDate_Yahoo(lis_Yahoo)
	# analysisEnDate_old(lis)

	time3 = time.perf_counter()
	print('analysis time : ' , (time3 - time2))
