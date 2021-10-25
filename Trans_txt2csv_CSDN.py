import sys
'''
Usage:
           参数：     
           CSV文件名    
           names自定义表头，可以换成任何内容 比如username mail passwd  
           sep指定分隔符，这里用制表符
           需要注意CSDN的csv有三列数据
    data = pd.read_csv('csdn-original-username-mail-passwd.csv', names=["用户名", "邮箱", "密码"], sep="\t")
    passwdList = pd.Series(data['密码'].values)
        
    这里Series读取一列数据，具体哪一列由表头指定，这里读了“密码” 这一列，如果上面names写的是passwd，这里就写passwd   
'''

if __name__ == '__main__':
    f = open("csdn.txt", 'r', encoding="utf-8")
    o = open("csdn-original-username-mail-passwd.csv", "w", encoding="utf-8")
    for line in f:
        username = line.split(" # ")[0]
        passwd = line.split(" # ")[1]
        mail = line.split(" # ")[2][:-1]
        o.write(username + "\t" + mail + "\t" + passwd + "\n")
    f.close()
    o.close()
