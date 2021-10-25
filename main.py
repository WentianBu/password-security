# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys

import configparser
import time
import re

import pandas as pd
from pandas import Series, DataFrame


# 统计可能含日期的口令(连续数字位数大于等于4的)
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

        # r'D[4-9]|D\d{2}'
        if re.search(r'D[4-9]|D\d{2}', res):
            df.append(passwd)

    return df


# 统计含数字日期的口令
def analysisDate(data):
    datePasswd = {'yyyy': 0, 'yyyymm': 0, 'yyyymmdd': 0, 'mmddyyyy': 0, 'ddmmyyyy': 0, 'yymmdd': 0, 'mmddyy': 0,
                  'ddmmyy': 0, 'mmdd': 0}
    for i in data:
        # yyyy 1700-2200
        if re.search(r'1[7-9]\d{2}|2[0-1]\d{2}', i):
            datePasswd['yyyy'] += 1
        # yyyy-mm
        if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])', i):
            datePasswd['yyyymm'] += 1
        # yyyy-mm-dd
        if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', i):
            datePasswd['yyyymmdd'] += 1
        # mm-dd-yyyy
        if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(1[7-9]\d{2}|2[0-1]\d{2})', i):
            datePasswd['mmddyyyy'] += 1
        # dd-mm-yyyy
        if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])(1[7-9]\d{2}|2[0-1]\d{2})', i):
            datePasswd['ddmmyyyy'] += 1
        # yy-mm-dd
        if re.search(r'[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', i):
            datePasswd['yymmdd'] += 1
        # mm-dd-yy
        if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[0-9][0-9]', i):
            datePasswd['mmddyy'] += 1
        # dd-mm-yy
        if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])[0-9][0-9]', i):
            datePasswd['ddmmyy'] += 1
        # mm-dd
        if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', i):
            datePasswd['mmdd'] += 1
    print('-----------------Date Password----------------------')
    print(datePasswd)
    print('--------------------------------------------------')


# 含英文日期的口令
def analysisEnDate(data):
    f = open("csdn-endate-username-mail-passwd.csv", "w", encoding="utf-8")
    dic = ['Jan', 'January', 'Feb', 'February', 'Mar', 'March', 'Apr', 'April',
           'May', 'Jun', 'June', 'Jul', 'July', 'Aug', 'August', 'Sep', 'September',
           'Oct', 'October', 'Nov', 'November', 'Dec', 'December']

    passwdList = []

    for line in data:
        for i in dic:
            if i in str(line):
                passwdList.append(str(line))
                f.write(line + '\n')

    f.close()
    print('\n')
    print('-------------Sum of English Date------------------')
    print(len(passwdList))
    print('--------------------------------------------------')


# 只含日期密码的口令
def analysisDateOnly(data):
    f = open("csdn-dateonly-username-mail-passwd.csv", "w", encoding="utf-8")
    for line in data:
        if re.match(r'\d+$', line):
            if re.match(r'1[7-9]\d{2}|2[0-1]\d{2}$', line):
                f.write(line + '\n')
            elif re.match(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])$', line):
                f.write(line + '\n')
            elif re.match(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$', line):
                f.write(line + '\n')
            elif re.match(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$', line):
                f.write(line + '\n')
    f.close()


if __name__ == '__main__':
    # --------------------读文件模块--------------------#
    # 读取passwd
    data = pd.read_csv('csdn-original-username-mail-passwd.csv', names=["用户名", "邮箱", "密码"], sep="\t")
    passwdList = pd.Series(data['密码'].values)

    # --------------------统计模块--------------------#
    # 判断可能是日期类的口令
    lis = countProbPasswd(passwdList)
    # 分析含日期的口令个数 打印
    analysisDate(lis)
    # 分析含英文日期的口令
    analysisEnDate(lis)
    # 分析纯日期口令
    analysisDateOnly(lis)

