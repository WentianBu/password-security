import pandas as pd

class length_count(object):
    def __init__(self,passwdList):
        self.passwdList=passwdList
    def lengthcount(self):
        len_ana={}
        for passwd in self.passwdList:
            length=len(str(passwd))
            if length in len_ana.keys():
                len_ana[length]+=1
            else:
                len_ana[length]=1
        return len_ana

if __name__=='__main__':
    #读入数据
    data=pd.read_csv('D:/project/DataSet/Yahoo-original-mail-passwd.csv',sep='\t',names=["mails","passwd"], encoding='ISO-8859-1')
    passwdList=pd.Series(data['passwd'].values)
    #统计长度
    len_ana=length_count(passwdList).lengthcount()
    #按长度排序
    print(sorted(len_ana.items()))
    #按个数排序长度
    print(sorted(len_ana.items(),key=lambda i:(i[1],i[0]),reverse=True))


